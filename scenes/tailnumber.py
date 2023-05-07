from utilities.animator import Animator
from setup import colours, fonts, screen

from rgbmatrix import graphics

# Setup
BAR_STARTING_POSITION = (0, 20)
BAR_PADDING = 2

FLIGHT_TAIL_NO_POSITION = (1, 19)
FLIGHT_TAIL_NO_TEXT_HEIGHT = 6  # based on font size
FLIGHT_TAIL_NO_FONT = fonts.extrasmall

FLIGHT_TAIL_NUMBER_ALPHA_COLOUR = colours.BLUE
FLIGHT_TAIL_NUMBER_NUMERIC_COLOUR = colours.BLUE_LIGHT

class TailNumberScene(object):
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
            BAR_STARTING_POSITION[1] - (FLIGHT_TAIL_NO_TEXT_HEIGHT // 2),
            screen.WIDTH - 1,
            BAR_STARTING_POSITION[1] + (FLIGHT_TAIL_NO_TEXT_HEIGHT // 2),
            colours.BLACK,
        )

        # Draw flight number if available
        flight_tail_no_text_length = 0
        if (
            self._data[self._data_index]["registration"]
            and self._data[self._data_index]["registration"] != "N/A"
        ):
            tail_no = f'{self._data[self._data_index]["registration"]}'

            for ch in tail_no:
                ch_length = graphics.DrawText(
                    self.canvas,
                    FLIGHT_TAIL_NO_FONT,
                    FLIGHT_TAIL_NO_POSITION[0] + flight_tail_no_text_length,
                    FLIGHT_TAIL_NO_POSITION[1],
                    FLIGHT_TAIL_NUMBER_NUMERIC_COLOUR
                    if ch.isnumeric()
                    else FLIGHT_TAIL_NUMBER_ALPHA_COLOUR,
                    ch,
                )
                flight_no_text_length += ch_length