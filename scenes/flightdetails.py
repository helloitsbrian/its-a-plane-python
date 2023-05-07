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
            
        graphics.DrawText(
            self.canvas,
            fonts.extrasmall,
            DEPARTURE_TIME_INDEX[0],
            DEPARTURE_TIME_INDEX[1],
            DATA_INDEX_COLOUR,
            start_dt.strftime("%H:%M")
        )

        graphics.DrawText(
            self.canvas,
            fonts.extrasmall,
            ARRIVAL_TIME_INDEX[0],
            ARRIVAL_TIME_INDEX[1],
            DATA_INDEX_COLOUR,
            end_dt.strftime("%H:%M")
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
            colours.GREEN,
            )

    def _calculate_flight_duration_data(self):
        time_details = self._data[self._data_index]["time"]
        start_time = time_details["real"].get("departure")
        if not start_time:
            start_time = time_details["estimated"].get("departure")
        end_time = time_details["estimated"].get("arrival")
        if not end_time:
            end_time = start_time + time_details["scheduled"]["arrival"] - time_details["scheduled"]["departure"]
        now = int(datetime.datetime.now(tz=pytz.timezone("UTC")).timestamp())
        ratio_of_flight_completed = (now - start_time) / (end_time - start_time)
        return self._timestamp_to_local_datetime(start_time), ratio_of_flight_completed, self._timestamp_to_local_datetime(end_time)
    
    def _timestamp_to_local_datetime(self, ts):
        return datetime.datetime.utcfromtimestamp(ts).replace(tzinfo = pytz.utc).astimezone(LOCAL_TZ)