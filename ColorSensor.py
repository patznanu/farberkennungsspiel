import board
import adafruit_tcs34725
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES, hex_to_rgb
from time import sleep

class ColorSensor():
    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = adafruit_tcs34725.TCS34725(self.i2c)

    def Close(self):
        del self.sensor

        try:
            self.i2c.deinit()
        except AttributeError:
            pass
        
        self.i2c = None

    def GetColorName(self):
        rgb = self.GetColorRgb()

        try:
            return rgb_to_name(rgb)
        except ValueError:
            closest_color = min(CSS3_HEX_TO_NAMES, key=lambda hex: sum((a - b) ** 2 for a, b in zip(rgb, hex_to_rgb(hex))))
            return CSS3_HEX_TO_NAMES[closest_color]

    def GetColorRgb(self):
        return self.sensor.color_rgb_bytes
