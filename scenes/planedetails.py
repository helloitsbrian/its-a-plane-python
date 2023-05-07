from rgbmatrix import graphics

from utilities.animator import Animator
from setup import colours, fonts, screen

# Setup
PLANE_DETAILS_COLOUR = colours.WHITE
PLANE_DISTANCE_FROM_TOP = 31
PLANE_TEXT_HEIGHT = 6
PLANE_FONT = fonts.small
PLANE_DISPLAY_START_POSITION = 5

class PlaneDetailsScene(object):
    def __init__(self):
        super().__init__()
        self.reset_scrolling()
        self.foo = 0
        self._data_all_looped = False

    @Animator.KeyFrame.add(1)
    def plane_details(self, count):

        # Guard against no data
        if len(self._data) == 0:
            return

        plane = f'{self._data[self._data_index]["plane"]}'

        # Draw background
        self.draw_square(
            0,
            PLANE_DISTANCE_FROM_TOP - PLANE_TEXT_HEIGHT,
            screen.WIDTH,
            screen.HEIGHT,
            colours.BLACK,
        )

        # Draw text
        text_length = graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.draw_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane,
        )

        # Handle scrolling 
        self.foo += 1
        if self.foo > 20:
            self.reset_scrolling()
            if len(self._data) > 1:
                self._data_index = (self._data_index + 1) % len(self._data)
                self._data_all_looped = (not self._data_index) or self._data_all_looped
                self.reset_scene()

    @Animator.KeyFrame.add(0)
    def reset_scrolling(self):
        self.foo = 0
