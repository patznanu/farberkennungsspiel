from smbus import SMBus
from PIL import ImageFont
from lib_oled96 import ssd1306


class OledDisplay():
    def __init__(self):
        self.__i2cbus = SMBus(1)
        self.__oled = ssd1306(self.__i2cbus)
        self.__canvas = self.__oled.canvas

        self.__fontHeader = ImageFont.truetype("FreeSans.ttf", 16)
        self.__fontText = ImageFont.truetype("FreeSans.ttf", 12)

        self.ClearDisplay()
        
    def ClearDisplay(self):
        self.__oled.cls()
        self.__oled.display()

    def WriteHeader(self, x, y, text):
        self.__canvas.text((x, y), text, font=self.__fontHeader, fill=1)

    def WriteText(self, x, y, text):
        self.__canvas.text((x, y), text, font=self.__fontText, fill=1)

    def ShowTexts(self) -> None:
        self.__oled.display()

    def DisplayMainMenu(self):
        self.ClearDisplay()
        self.WriteHeader(0, 0, "Hauptmenü")
        self.WriteText(10, 20, "-> Farbe einscannen")
        self.WriteText(10, 30, "-> Farbmemory")
        self.WriteText(10, 50, "-> Beenden")
        self.ShowTexts()