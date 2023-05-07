from rgbmatrix import graphics

from utilities.animator import Animator
from setup import colours, fonts, screen

# Setup
REG_DETAILS_COLOUR = colours.WHITE
REG_DISTANCE_FROM_TOP = 30
REG_TEXT_HEIGHT = 6
REG_FONT = fonts.extrasmall

class RegDetailsScene(object):
    def __init__(self):
        super().__init__()
        self.plane_position = screen.WIDTH
        self._data_all_looped = False

    @Animator.KeyFrame.add(1)
    def plane_details(self, count):

        # Guard against no data
        if len(self._data) == 0:
            return

        reg = f'{self._data[self._data_index]["reg"]}'

        # Draw background
        self.draw_square(
            0,
            REG_DISTANCE_FROM_TOP - REG_TEXT_HEIGHT,
            screen.WIDTH,
            screen.HEIGHT,
            colours.BLACK,
        )

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            REG_FONT,
            self.plane_position,
            REG_DISTANCE_FROM_TOP,
            REG_DETAILS_COLOUR,
            reg,
        )

        # Handle scrolling
        self.plane_position -= 1
        if self.plane_position + text_length < 0:
            self.plane_position = screen.WIDTH
            if len(self._data) > 1:
                self._data_index = (self._data_index + 1) % len(self._data)
                self._data_all_looped = (not self._data_index) or self._data_all_looped
                self.reset_scene()

    @Animator.KeyFrame.add(0)
    def reset_scrolling(self):
        self.plane_position = screen.WIDTH