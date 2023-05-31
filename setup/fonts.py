import os
from rgbmatrix import graphics

# Fonts
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
extrasmall = graphics.Font()
small = graphics.Font()
regular = graphics.Font()
regular_bold = graphics.Font()
large = graphics.Font()
large_bold = graphics.Font()
super_large_bold = graphics.Font()
extrasmall.LoadFont(f"{DIR_PATH}/../fonts/4x6.bdf")
small.LoadFont(f"{DIR_PATH}/../fonts/5x8.bdf")
regular.LoadFont(f"{DIR_PATH}/../fonts/6x12.bdf")
regular_bold.LoadFont(f"{DIR_PATH}/../fonts/6x13B.bdf")
large.LoadFont(f"{DIR_PATH}/../fonts/8x13.bdf")
large_bold.LoadFont(f"{DIR_PATH}/../fonts/8x13B.bdf")
super_large_bold.LoadFont(f"{DIR_PATH}/../fonts/9x18B.bdf")
