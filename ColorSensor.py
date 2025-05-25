import adafruit_tcs34725
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES, hex_to_rgb

class ColorSensor():
    def __init__(self, i2c):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)

    def GetColorName(self):
        rgb = self.GetColorRgb()

        try:
            return rgb_to_name(rgb)
        except ValueError:
            closest_color = min(CSS3_HEX_TO_NAMES, key=lambda hex: sum((a - b) ** 2 for a, b in zip(rgb, hex_to_rgb(hex))))
            return CSS3_HEX_TO_NAMES[closest_color]

    def GetColorRgb(self):
        return self.sensor.color_rgb_bytes
