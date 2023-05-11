from FlightRadar24.api import FlightRadar24API
from threading import Thread, Lock
from time import sleep
import math
import pprint

try:
    # Attempt to load config data
    from config import MIN_ALTITUDE

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    MIN_ALTITUDE = 0  # feet

RETRIES = 3
RATE_LIMIT_DELAY = 1
MAX_FLIGHT_LOOKUP = 5
MAX_ALTITUDE = 41000  # feet
EARTH_RADIUS_KM = 6371
BLANK_FIELDS = ["", "N/A", "NONE"]
ALLOWED_AIRCRAFT_CODES = ["B77W","B738","DH8D","B789","B739","E75L","A320","A321","A333","A319","A359","BCS1","A20N","A339","CRJ7","B752","B763","BCS3","A21N","B712","B753","B332","A318","A19N","A343","A346","A35K","A388","B37M","B38M","B39M","B3XM","B732","B737","B744","B748","B764","B772","B773","B77L","B788","B78X","CRJ9","CRJ2","E145","E170","E190","E295"]

try:
    # Attempt to load config data
    from config import ZONE_HOME, LOCATION_HOME

    ZONE_DEFAULT = ZONE_HOME
    LOCATION_DEFAULT = LOCATION_HOME

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    ZONE_DEFAULT = {"tl_y": 62.61, "tl_x": -13.07, "br_y": 49.71, "br_x": 3.46}
    LOCATION_DEFAULT = [51.509865, -0.118092, EARTH_RADIUS_KM]


def distance_from_flight_to_home(flight, home=LOCATION_DEFAULT):
    def polar_to_cartesian(lat, long, alt):
        DEG2RAD = math.pi / 180
        return [
            alt * math.cos(DEG2RAD * lat) * math.sin(DEG2RAD * long),
            alt * math.sin(DEG2RAD * lat),
            alt * math.cos(DEG2RAD * lat) * math.cos(DEG2RAD * long),
        ]

    def feet_to_meters_plus_earth(altitude_ft):
        altitude_km = 0.0003048 * altitude_ft
        return altitude_km + EARTH_RADIUS_KM

    try:
        (x0, y0, z0) = polar_to_cartesian(
            flight.latitude,
            flight.longitude,
            feet_to_meters_plus_earth(flight.altitude),
        )

        (x1, y1, z1) = polar_to_cartesian(*home)

        dist = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2)

        return dist

    except AttributeError:
        # on error say it's far away
        return 1e6


class Overhead:
    def __init__(self):
        self._api = FlightRadar24API()
        self._lock = Lock()
        self._data = []
        self._new_data = False
        self._processing = False

    def grab_data(self):
        Thread(target=self._grab_data).start()

    def _flight_filter(self,f):
        return f.altitude < MAX_ALTITUDE and f.altitude > MIN_ALTITUDE and f.aircraft_code in ALLOWED_AIRCRAFT_CODES

    def _grab_data(self):
        # Mark data as old
        with self._lock:
            self._new_data = False
            self._processing = True

        data = []

        # Grab flight details
        bounds = self._api.get_bounds(ZONE_DEFAULT)
        flights = self._api.get_flights(bounds=bounds)

        # Sort flights by closest first
        flights = [
            f
            for f in flights
            if self._flight_filter(f)
        ]

        flights = sorted(flights, key=lambda f: distance_from_flight_to_home(f))

        for flight in flights[:MAX_FLIGHT_LOOKUP]:
            retries = RETRIES

            while retries:
                # Rate limit protection
                sleep(RATE_LIMIT_DELAY)

                # Grab and store details
                try:
                    details = self._api.get_flight_details(flight.id)

                    # Get plane model
                    try:
                        plane_model = details["aircraft"]["model"]["code"]
                    except (KeyError, TypeError):
                        plane_model = ""

                    # Get plane registration
                    try:
                        plane_registration = details["aircraft"]["registration"]
                    except (KeyError, TypeError):
                        plane_registration = ""

                    # Get scheduled departure time
                    try:
                        scheduled_departure = details["time"]["scheduled"]["departure"]
                    except (KeyError, TypeError):
                        scheduled_departure = ""

                    # Get actual departure time
                    try:
                        real_departure = details["time"]["real"]["departure"]
                    except (KeyError, TypeError):
                        real_departure = ""

                    # Get scheduled arrival time
                    try:
                        scheduled_arrival = details["time"]["scheduled"]["arrival"]
                    except (KeyError, TypeError):
                        scheduled_arrival = ""

                    # Get estimated arrival time
                    try:
                        est_arrival = details["time"]["estimated"]["arrival"]
                    except (KeyError, TypeError):
                        est_arrival = ""
                    
                    pprint.pprint(scheduled_departure)
                    pprint.pprint(real_departure)
                    pprint.pprint(scheduled_arrival)
                    pprint.pprint(est_arrival)

                    # Tidy up what we pass along
                    plane_model = plane_model if not (plane_model.upper() in BLANK_FIELDS) else ""
                    plane_registration = plane_registration if not (plane_registration.upper() in BLANK_FIELDS) else ""

                    origin = (
                        flight.origin_airport_iata
                        if not (flight.origin_airport_iata.upper() in BLANK_FIELDS)
                        else ""
                    )

                    destination = (
                        flight.destination_airport_iata
                        if not (flight.destination_airport_iata.upper() in BLANK_FIELDS)
                        else ""
                    )

                    callsign = (
                        flight.callsign
                        if not (flight.callsign.upper() in BLANK_FIELDS)
                        else ""
                    )

                    data.append(
                        {
                            "plane_model": plane_model,
                            "plane_registration": plane_registration,
                            "origin": origin,
                            "destination": destination,
                            "vertical_speed": flight.vertical_speed,
                            "altitude": flight.altitude,
                            "callsign": callsign,
                            # "time": details["time"],
                        }
                    )
                    break

                except (KeyError, AttributeError):
                    retries -= 1

        with self._lock:
            self._new_data = True
            self._processing = False
            self._data = data

    @property
    def new_data(self):
        with self._lock:
            return self._new_data

    @property
    def processing(self):
        with self._lock:
            return self._processing

    @property
    def data(self):
        with self._lock:
            self._new_data = False
            return self._data

    @property
    def data_is_empty(self):
        return len(self._data) == 0


# Main function
if __name__ == "__main__":

    o = Overhead()
    o.grab_data()
    while not o.new_data:
        print("processing...")
        sleep(1)

    print(o.data)
