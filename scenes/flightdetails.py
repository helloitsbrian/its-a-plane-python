from utilities.animator import Animator
from setup import colours, fonts, screen 
import datetime
import pytz

from rgbmatrix import graphics

# Setup
FLIGHT_DETAILS_BAR_STARTING_POSITION = (0, 15)
FLIGHT_PROGRESS_BAR_HEIGHT = 5
BAR_HPADDING = 2
BAR_VPADDING = 1

FLIGHT_NO_POSITION = (1, 18)
FLIGHT_NO_TEXT_HEIGHT = 6  # based on font size
FLIGHT_NO_FONT = fonts.small

FLIGHT_NUMBER_ALPHA_COLOUR = colours.BLUE
FLIGHT_NUMBER_NUMERIC_COLOUR = colours.BLUE_LIGHT

DATA_INDEX_POSITION = (49, 18)
DATA_INDEX_TEXT_HEIGHT = 6
DATA_INDEX_FONT = fonts.small

DIVIDING_BAR_COLOUR = colours.GREEN
DATA_INDEX_COLOUR = colours.GREY

TOP_OF_PROGRESS_SECTION = FLIGHT_DETAILS_BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2) + BAR_VPADDING
BOTTOM_OF_PROGRESS_SECTION = FLIGHT_DETAILS_BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2) + BAR_VPADDING + FLIGHT_PROGRESS_BAR_HEIGHT
DEPARTURE_TIME_INDEX = (1, BOTTOM_OF_PROGRESS_SECTION)
ARRIVAL_TIME_INDEX = (screen.WIDTH - 20, BOTTOM_OF_PROGRESS_SECTION)
PROGRESS_BAR_INDEX = (22,(TOP_OF_PROGRESS_SECTION + BOTTOM_OF_PROGRESS_SECTION) // 2)
DEFAULT_BAR_PROGRESS = 0.5
DELAYED_COLOUR = colours.RED_LIGHT
DELAY_TIME_WINDOW_SECONDS = 1800

LOCAL_TZ = pytz.timezone("America/Denver")


class FlightDetailsScene(object):
    def __init__(self):
        super().__init__()

    @Animator.KeyFrame.add(0)
    def flight_details(self):

        # Guard against no data
        if len(self._data) == 0:
            return

        # Clear the whole area
        self.draw_square(
            0,
            FLIGHT_DETAILS_BAR_STARTING_POSITION[1] - (FLIGHT_NO_TEXT_HEIGHT // 2),
            screen.WIDTH - 1,
            BOTTOM_OF_PROGRESS_SECTION,
            colours.BLACK,
        )

        # Draw flight number if available
        flight_no_text_length = 0
        if (
            self._data[self._data_index]["callsign"]
            and self._data[self._data_index]["callsign"] != "N/A"
        ):
            flight_no = f'{self._data[self._data_index]["callsign"]}'

            for ch in flight_no:
                ch_length = graphics.DrawText(
                    self.canvas,
                    FLIGHT_NO_FONT,
                    FLIGHT_NO_POSITION[0] + flight_no_text_length,
                    FLIGHT_NO_POSITION[1],
                    FLIGHT_NUMBER_NUMERIC_COLOUR
                    if ch.isnumeric()
                    else FLIGHT_NUMBER_ALPHA_COLOUR,
                    ch,
                )
                flight_no_text_length += ch_length

        # Draw bar
        if len(self._data) > 1:
            # Clear are where N of M might have been
            self.draw_square(
                DATA_INDEX_POSITION[0] - BAR_VPADDING,
                FLIGHT_DETAILS_BAR_STARTING_POSITION[1] - (FLIGHT_NO_TEXT_HEIGHT // 2),
                screen.WIDTH,
                FLIGHT_DETAILS_BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2),
                colours.BLACK,
            )

        #     # Dividing bar
        #     graphics.DrawLine(
        #         self.canvas,
        #         flight_no_text_length + BAR_VPADDING,
        #         FLIGHT_DETAILS_BAR_STARTING_POSITION[1],
        #         DATA_INDEX_POSITION[0] - BAR_VPADDING - 1,
        #         FLIGHT_DETAILS_BAR_STARTING_POSITION[1],
        #         DIVIDING_BAR_COLOUR,
        #     )

            # Draw text
            text_length = graphics.DrawText(
                self.canvas,
                fonts.small,
                DATA_INDEX_POSITION[0],
                DATA_INDEX_POSITION[1],
                DATA_INDEX_COLOUR,
                f"{self._data_index + 1}/{len(self._data)}",
            )

        # else:
        #     # Dividing bar
        #     graphics.DrawLine(
        #         self.canvas,
        #         flight_no_text_length + BAR_VPADDING if flight_no_text_length else 0,
        #         FLIGHT_DETAILS_BAR_STARTING_POSITION[1],
        #         screen.WIDTH,
        #         FLIGHT_DETAILS_BAR_STARTING_POSITION[1],
        #         DIVIDING_BAR_COLOUR,
            
        #     )
            
        self._draw_progress_data()
        
    def _draw_progress_data(self):
        start_dt, ratio_completed, end_dt = self._calculate_flight_duration_data()
        departure_time_colour = DATA_INDEX_COLOUR
        arrival_time_colour = DATA_INDEX_COLOUR
        progress_bar_colour = DIVIDING_BAR_COLOUR

        scheduled_departure_time = self._data[self._data_index]["scheduled_departure"]
        real_departure_time = self._data[self._data_index]["real_departure"]
        scheduled_arrival_time = self._data[self._data_index]["scheduled_arrival"]
        estimated_arrival_time = self._data[self._data_index]["estimated_arrival"]

        if real_departure_time and real_departure_time > (scheduled_departure_time + DELAY_TIME_WINDOW_SECONDS):
            departure_time_colour = DELAYED_COLOUR

        if estimated_arrival_time and estimated_arrival_time > (scheduled_arrival_time + DELAY_TIME_WINDOW_SECONDS):
            arrival_time_colour = DELAYED_COLOUR
            progress_bar_colour = DELAYED_COLOUR

        if isinstance(start_dt, datetime.datetime):      
            graphics.DrawText(
                self.canvas,
                fonts.extrasmall,
                DEPARTURE_TIME_INDEX[0],
                DEPARTURE_TIME_INDEX[1],              
                departure_time_colour,
                start_dt.strftime("%H:%M")
            )
        else:
            graphics.DrawText(
                self.canvas,
                fonts.extrasmall,
                DEPARTURE_TIME_INDEX[0],
                DEPARTURE_TIME_INDEX[1],              
                departure_time_colour,
                " N/A "
            )

        if isinstance(end_dt, datetime.datetime):
            graphics.DrawText(
                self.canvas,
                fonts.extrasmall,
                ARRIVAL_TIME_INDEX[0],
                ARRIVAL_TIME_INDEX[1],            
                arrival_time_colour,
                end_dt.strftime("%H:%M")
            )
        else:
            graphics.DrawText(
                self.canvas,
                fonts.extrasmall,
                ARRIVAL_TIME_INDEX[0],
                ARRIVAL_TIME_INDEX[1],            
                arrival_time_colour,
                " N/A "
            )

        graphics.DrawLine(
            self.canvas,
            PROGRESS_BAR_INDEX[0],
            PROGRESS_BAR_INDEX[1],
            PROGRESS_BAR_INDEX[0] + 19,
            PROGRESS_BAR_INDEX[1],
            colours.WHITE,
        )

        graphics.DrawLine(
            self.canvas,
            PROGRESS_BAR_INDEX[0],
            PROGRESS_BAR_INDEX[1],
            PROGRESS_BAR_INDEX[0] + min([18, int(19 * ratio_completed)]),
            PROGRESS_BAR_INDEX[1],
            progress_bar_colour,
        )

    def _calculate_flight_duration_data(self):
        # Get the flight time details
        start_time = self._data[self._data_index]["real_departure"]
        scheduled_departure_time = self._data[self._data_index]["scheduled_departure"]
        scheduled_arrival_time = self._data[self._data_index]["scheduled_arrival"]
        end_time = self._data[self._data_index]["estimated_arrival"]
        journey_time = 0

        now = datetime.datetime.now(tz=pytz.timezone("UTC"))

        # Determine the start time, if there is "None" start time, assign None
        if start_time is not None:
            start_time = self._timestamp_to_local_datetime(start_time)
        elif scheduled_departure_time is not None:
            start_time = scheduled_departure_time
        else:
            start_time = None

        # Build the calculation for journey time, if variables are available
        if scheduled_departure_time is not None and scheduled_arrival_time is not None:
            journey_time = scheduled_arrival_time - scheduled_departure_time

        if scheduled_departure_time is not None:
            scheduled_departure_time = self._timestamp_to_local_datetime(scheduled_departure_time)
        else:
            scheduled_departure_time = None

        if scheduled_arrival_time is not None:
            scheduled_arrival_time = self._timestamp_to_local_datetime(scheduled_arrival_time)
        else:
            scheduled_arrival_time = None

        if end_time is not None:
            end_time = self._timestamp_to_local_datetime(end_time)
        elif scheduled_arrival_time is not None:
            end_time = scheduled_arrival_time
        else:
            end_time = None

        if end_time is None:
            ratio_of_flight_completed = DEFAULT_BAR_PROGRESS
        elif abs((end_time - start_time).total_seconds()) == 0:
            ratio_of_flight_completed = DEFAULT_BAR_PROGRESS
        else:
            ratio_of_flight_completed = (now - start_time).total_seconds() / (end_time - start_time).total_seconds()

        return start_time, ratio_of_flight_completed, end_time
    
    def _timestamp_to_local_datetime(self, ts):
        return datetime.datetime.utcfromtimestamp(ts).replace(tzinfo = pytz.utc).astimezone(LOCAL_TZ)