#!/usr/bin/env python3
from PIL import Image
import ST7789
import time
import sys

print("""
gif.py - Display a gif on the LCD.

If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the front slot.

""")

if len(sys.argv) < 2:
    print("""Usage: {path} <gif_file> <display_type>

Where <gif_file> is a .gif file.
  Hint: {path} deployrainbows.gif

And <display_type> is one of:
  * square - 240x240 1.3" Square LCD
  * round  - 240x240 1.3" Round LCD (applies an offset)
""".format(path=sys.argv[0]))
    sys.exit(1)

image_file = sys.argv[1]

try:
    display_type = sys.argv[2]
except IndexError:
    display_type = "square"

# Create TFT LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=40 if display_type == "round" else 0
)

# Initialize display.
disp.begin()

width = disp.width
height = disp.height

# Load an image.
print('Loading gif: {}...'.format(image_file))
image = Image.open(image_file)

print('Drawing gif, press Ctrl+C to exit!')

frame = 0

while True:
    try:
        image.seek(frame)
        disp.display(image.resize((width, height)))
        frame += 1
        time.sleep(0.05)

    except EOFError:
        frame = 0
