from rgbmatrix import graphics

from utilities.animator import Animator
from setup import colours, fonts, screen

# Setup
PLANE_DETAILS_COLOUR = colours.WHITE
PLANE_DISTANCE_FROM_TOP = 31
PLANE_TEXT_HEIGHT = 6
PLANE_FONT = fonts.small
PLANE_DISPLAY_START_POSITION = 5
PLANE_CLOCK_SPEED = 100
SEPARATOR_TEXT = "·"

class PlaneDetailsScene(object):
    def __init__(self):
        super().__init__()
        self.reset_scrolling()
        self._plane_clock = 0
        self._data_all_looped = False

    @Animator.KeyFrame.add(1)
    def plane_details(self, count):

        # Guard against no data
        if len(self._data) == 0:
            return

        plane_model = f'{self._data[self._data_index]["plane_model"]}'
        plane_registration = f'{self._data[self._data_index]["plane_registration"]}'

        # Draw background
        self.draw_square(
            0,
            PLANE_DISTANCE_FROM_TOP - PLANE_TEXT_HEIGHT,
            screen.WIDTH,
            screen.HEIGHT,
            colours.BLACK,
        )

        model_width = graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.draw_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane_model,
        )

        registration_width = graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.draw_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane_registration,
        )

        separator_width = graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.draw_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            SEPARATOR_TEXT,
        )

        # Draw ICAO plane model text
        graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            self.draw_position,
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane_model,
        )

        graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            (self.draw_position + model_width),
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            SEPARATOR_TEXT,            
        )

        # Draw plane tail number text
        graphics.DrawText(
            self.canvas,
            PLANE_FONT,
            (self.draw_position + model_width + separator_width),
            PLANE_DISTANCE_FROM_TOP,
            PLANE_DETAILS_COLOUR,
            plane_registration,
        )

        # Handle scrolling 
        self._plane_clock += 1
        if self._plane_clock > PLANE_CLOCK_SPEED:
            self.reset_scrolling()
            if len(self._data) > 1:
                self._data_index = (self._data_index + 1) % len(self._data)
                self._data_all_looped = (not self._data_index) or self._data_all_looped
                self.reset_scene()

    @Animator.KeyFrame.add(0)
    def reset_scrolling(self):
        self.draw_position = PLANE_DISPLAY_START_POSITION
        self._plane_clock = 0
