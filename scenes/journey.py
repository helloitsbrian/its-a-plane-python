from utilities.animator import Animator
from setup import colours, fonts

from rgbmatrix import graphics

# Attempt to load config data
try:
    from config import JOURNEY_CODE_SELECTED

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    JOURNEY_CODE_SELECTED = "GLA"

try:
    from config import JOURNEY_BLANK_FILLER

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    JOURNEY_BLANK_FILLER = " ? "

# Setup
JOURNEY_POSITION = (0, 0)
JOURNEY_HEIGHT = 10
JOURNEY_WIDTH = 64
JOURNEY_SPACING = 21
JOURNEY_FONT = fonts.regular_bold
JOURNEY_FONT_SELECTED = fonts.regular_bold
JOURNEY_COLOUR = colours.WHITE
SELECTED_COLOUR = colours.YELLOW_DARK
ARROW_COLOUR = colours.WHITE

# Element Positions
ARROW_POINT_POSITION = (33, 5)
ARROW_WIDTH = 3
ARROW_HEIGHT = 6


class JourneyScene(object):
    def __init__(self):
        super().__init__()

    @Animator.KeyFrame.add(0)
    def journey(self):
        # Guard against no data
        if len(self._data) == 0:
            return

        origin = self._data[self._data_index]["origin"]
        destination = self._data[self._data_index]["destination"]

        # Draw background
        self.draw_square(
            JOURNEY_POSITION[0],
            JOURNEY_POSITION[1],
            JOURNEY_POSITION[0] + JOURNEY_WIDTH,
            JOURNEY_POSITION[1] + JOURNEY_HEIGHT,
            colours.JOURNEY_BLUE,
        )

        # Draw origin
        text_length = graphics.DrawText(
            self.canvas,
            JOURNEY_FONT_SELECTED if origin == JOURNEY_CODE_SELECTED else JOURNEY_FONT,
	        2,
            JOURNEY_HEIGHT,
            SELECTED_COLOUR if origin == JOURNEY_CODE_SELECTED else JOURNEY_COLOUR,
            origin if origin else JOURNEY_BLANK_FILLER,
        )

        # Draw destination
        _ = graphics.DrawText(
            self.canvas,
            JOURNEY_FONT_SELECTED
	    if destination == JOURNEY_CODE_SELECTED
	    else JOURNEY_FONT,
            text_length + JOURNEY_SPACING,
            JOURNEY_HEIGHT,
            SELECTED_COLOUR if destination == JOURNEY_CODE_SELECTED else JOURNEY_COLOUR,
            destination if destination else JOURNEY_BLANK_FILLER,
        )

    @Animator.KeyFrame.add(0)
    def journey_arrow(self):
        # Guard against no data
        if len(self._data) == 0:
            return

        # Black area before arrow
        self.draw_square(
            ARROW_POINT_POSITION[0] - ARROW_WIDTH,
            ARROW_POINT_POSITION[1] - (ARROW_HEIGHT // 2),
            ARROW_POINT_POSITION[0],
            ARROW_POINT_POSITION[1] + (ARROW_HEIGHT // 2),
            colours.JOURNEY_BLUE,
        )

        # Starting positions for filled in arrow
        x = ARROW_POINT_POSITION[0] - ARROW_WIDTH
        y1 = ARROW_POINT_POSITION[1] - (ARROW_HEIGHT // 2)
        y2 = ARROW_POINT_POSITION[1] + (ARROW_HEIGHT // 2)

        # Tip of arrow
        self.canvas.SetPixel(
            ARROW_POINT_POSITION[0],
            ARROW_POINT_POSITION[1],
            ARROW_COLOUR.red,
            ARROW_COLOUR.green,
            ARROW_COLOUR.blue,
        )

        # Draw using columns
        for col in range(0, ARROW_WIDTH):
            graphics.DrawLine(
                self.canvas,
                x,
                y1,
                x,
                y2,
                ARROW_COLOUR,
            )

            # Calculate next column's data
            x += 1
            y1 += 1
            y2 -= 1
