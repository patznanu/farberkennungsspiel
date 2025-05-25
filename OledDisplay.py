from smbus import SMBus
from PIL import ImageFont
from time import sleep
from lib_oled96 import ssd1306

class OledDisplay():
    def __init__(self):
        self.i2cbus = SMBus(1)
        self.oled = ssd1306(self.i2cbus)
        self.canvas = self.oled.canvas

        self.fontHeader = ImageFont.truetype("FreeSans.ttf", 16)
        self.fontText = ImageFont.truetype("FreeSans.ttf", 12)
        self.fontOverlay = ImageFont.truetype("FreeSans.ttf", 24)

        self.menuOffset = 20
        self.menuOrder = [50, 20, 30]

        self.ClearDisplay()

    def Close(self):
        self.i2cbus.close()
        self.oled = None
        self.i2cbus = None
        sleep(1)
        
    def ClearDisplay(self):
        self.oled.cls()
        self.oled.display()

    def ShowMenuMain(self, selectedMenu):
        self.ClearDisplay()
        self.WriteHeader(0, 0, "Hauptmenü")
        self.WriteText(self.menuOffset, self.menuOrder[1], "-> Farbe einscannen")
        self.WriteText(self.menuOffset, self.menuOrder[2], "-> Farbmemory")
        self.WriteText(self.menuOffset, self.menuOrder[0], "-> Beenden")
        self.WriteSelectedMenu(selectedMenu)
        self.ShowTexts()

    def WriteHeader(self, x, y, text):
        self.canvas.text((x, y), text, font=self.fontHeader, fill=1)

    def WriteText(self, x, y, text):
        self.canvas.text((x, y), text, font=self.fontText, fill=1)

    def ShowTexts(self) -> None:
        self.oled.display()
    
    def WriteSelectedMenu(self, selectedMenu):
        self.canvas.text((self.menuOffset/2, self.menuOrder[selectedMenu]), "#", fill=1)

    def ShowError(self):
        self.ClearDisplay()
        self.WriteText(10, 10, "Error")
        self.ShowTexts()

    def ShowSelectedMenu(self, text):
        self.ClearDisplay()
        self.canvas.text((10, 10), text, font=self.fontOverlay, fill=1)
        self.ShowTexts()
        sleep(2)
        self.ClearDisplay()
        self.ShowTexts()

    def ShowMenuScanner(self, selectedMenu, color=""):
        self.ClearDisplay()
        self.WriteHeader(0, 0, "Farbe")
        self.WriteText(self.menuOffset, self.menuOrder[1], "-> Farbe einscannen")
        self.WriteText(self.menuOffset, self.menuOrder[2], f"   Farbe: {color}")
        self.WriteText(self.menuOffset, self.menuOrder[0], "-> Beenden")
        self.WriteSelectedMenu(selectedMenu)
        self.ShowTexts()

    def InstructionsScanner(self):
        self.ClearDisplay()
        self.WriteHeader(0, 0, "Scanner")
        self.WriteText(self.menuOffset, self.menuOrder[1], "Knopf drücken um Farbe einzulesen")
        self.ShowTexts()

    def ShowLog(self, text):
        self.ClearDisplay()
        self.WriteText(0, 0, text)
        self.ShowTexts()
