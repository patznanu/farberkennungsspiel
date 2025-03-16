"""from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

oled_font = ImageFont.truetype('FreeSans.ttf', 14)
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline = "white", fill = "black")
    draw.text((10, 10), "Hello Welt!", font = oled_font, fill = "white")
"""

"""
from lib_oled96 import ssd1306
from smbus import SMBus

i2cbus = SMBus(1)
oled = ssd1306(i2cbus)

draw = oled.canvas

oled.cls()
oled.display()

draw.text((20, 16), "Hallo", fill=1)
draw.text((60, 16), "Welt", fill=1)

oled.display()
"""

import board
import adafruit_tcs34725
from time import sleep
from webcolors import rgb_to_name

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

while True:
    try:
        print(webcolors.rgb_to_name(sensor.color_rgb_bytes))
    except:
        print("Nicht erkannt")
    #print(sensor.color_raw)
    #print(sensor.color_temperature)

    sleep(3)