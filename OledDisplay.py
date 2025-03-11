from lib_oled96 import ssd1306
from smbus import SMBus

class OledDisplay():
    def __init__(self):
        self.__i2cbus = SMBus(1)
        self.__oled = ssd1306(self.__i2cbus)
        self.__canvas = self.__oled.canvas
        self.ClearDisplay()
        
    def ClearDisplay(self) -> None:
        self.__oled.cls()
        self.__oled.display()

    def Write(self, x: int, y: int, text: str, fill: int) -> None:
        self.__canvas.text((x, y), text, fill)

    def ShowTexts(self) -> None:
        self.__oled.display()
