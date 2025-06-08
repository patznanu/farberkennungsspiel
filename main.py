from random import randrange
from OledDisplay import OledDisplay
from RotaryEncoder import RotaryEncoder
from ColorSensor import ColorSensor

def RunMenuMain():
    DisplayMainMenu()
    while True:
        match SelectingMenu(1, 2):
            case 1:
                RunMenuScanner()
            case 2:
                RunGameMemory()
            case _:
                return
            
def DisplayMainMenu():
    display = OledDisplay()
    display.ShowSelectedMenu("Menü")
    display.MainMenu(1)
    display.Close()

def SelectingMenu(menu, maxMenues):
    rotaryEncoder = RotaryEncoder()
    display = OledDisplay()
    selectedMenu = 1
    isSelectingMenu = True
    lastClock = rotaryEncoder.GetClockInput()
    
    if menu == 1:
        display.MainMenu(selectedMenu)

    while isSelectingMenu:
        if rotaryEncoder.IsButtonPressed():
            isSelectingMenu = False
        else:
            currentClock = rotaryEncoder.GetClockInput()
            currentDirection = rotaryEncoder.GetDirectionInput()
            if currentClock != lastClock:
                if currentDirection != currentClock:
                    selectedMenu -= 1  # Clockwise
                else:
                    selectedMenu += 1  # Counter-clockwise
                lastClock = currentClock
                selectedMenu = Clamp(selectedMenu, 0, maxMenues)
                if menu == 1:
                    display.MainMenu(selectedMenu)
                elif menu == 2:
                    display.ScannerMenu(selectedMenu)
    rotaryEncoder.Close()
    display.Close()
    return selectedMenu

def RunMenuScanner():
    display = OledDisplay()
    display.ShowSelectedMenu("Scanner")
    display.ScannerMenu(1)

    match SelectingMenu(2, 1):
        case 1:
            RunGameScanner()
            display.Close()
        case _:
            display.Close()
            return

def RunGameScanner():
    WatilTilButtonPressed()
    DisplayShowMenuScanner(GetColorName())

def WatilTilButtonPressed():
    rotaryEncoder = RotaryEncoder()
    isButtonPressed = False

    while not isButtonPressed:
        isButtonPressed = rotaryEncoder.IsButtonPressed()

    rotaryEncoder.Close()

def GetColorName():
    colorSensor = ColorSensor()
    color = colorSensor.GetColorName()
    colorSensor.Close()
    return color

def DisplayShowMenuScanner(colorName):
    display = OledDisplay()
    display.ScannerMenu(1, colorName)
    display.Close()

def RunGameMemory():
    rotaryEncoder = RotaryEncoder()
    list = []
    list.append(AddEntry())
    maxPoints = 5
    currentPoints = 0
    isGameRunning = True
    didWin = False

    while isGameRunning:
        if currentPoints < maxPoints:
            i = 0
            while i < len(list):
                while not isButtonPressed:
                    isButtonPressed = rotaryEncoder.IsButtonPressed()

                rgb = GetColorRGB()
                buffer = 20
                r = rgb[0]-buffer <= list[i][0] <= rgb[0]+buffer
                g = rgb[1]-buffer <= list[i][1] <= rgb[1]+buffer
                b = rgb[2]-buffer <= list[i][2] <= rgb[2]+buffer

                if r and g and b:
                    i += 1
                    list.append(AddEntry())
                else:
                    DisplayShowLog("Verlierer")
                    isGameRunning = False
                    i = len(list)
        else:
            DisplayShowLog("Gewinner")
            isGameRunning = False
            didWin = True
    rotaryEncoder.Close()
    return didWin

def Clamp(number, min, max):
    if (number < min):
        return max
    if number > max:
        return min
    return number

def AddEntry():
    entry = []
    entry.append(randrange(255))
    entry.append(randrange(255))
    entry.append(randrange(255))
    return entry

def GetColorRGB():
    colorSensor = ColorSensor()
    color = colorSensor.GetColorRgb()
    colorSensor.Close()
    return color

def DisplayShowLog(text):
    display = OledDisplay()
    display.ShowLog(text)
    display.Close()

if __name__ == "__main":
    RunMenuMain()
