from random import randrange
from OledDisplay import OledDisplay
from RotaryEncoder import RotaryEncoder
from ColorSensor import ColorSensor


def Main():
    RunMenuMain()

def RunMenuMain():
    global display
    display.ShowSelectedMenu("Menü")
    display.ShowMenuMain(1)

    while True:
        match MenuSelectionMain():
            case 1:
                RunMenuScanner()
            case 2:
                RunGameMemory()
            case _:
                return

def MenuSelectionMain():
    global display
    global rotaryEncoder
    
    selectedMenu = 1
    maxMenues = 2
    isSelectingMenu = True
    lastClock = rotaryEncoder.GetClockInput()

    while isSelectingMenu:
        if rotaryEncoder.IsButtonPressed():
            isSelectingMenu = False
        else:
            currentClock = rotaryEncoder.GetClockInput()
            currentDirection = rotaryEncoder.GetDirectionInput()

            if currentClock != lastClock:
                if currentDirection != currentClock:
                    selectedMenu += 1  # Clockwise
                else:
                    selectedMenu -= 1  # Counter-clockwise

                lastClock = currentClock
                selectedMenu = Clamp(selectedMenu, 0, maxMenues)
                display.ShowMenuMain(selectedMenu)

    return selectedMenu

def RunMenuScanner():
    global display
    display.ShowSelectedMenu("Scanner")
    display.ShowMenuScanner(1)

    match MenuSelectionScanner():
        case 1:
            RunGameScanner()
        case _:
            return

def MenuSelectionScanner():
    global display
    global rotaryEncoder
    
    selectedMenu = 1
    maxMenues = 1
    isSelectingMenu = True
    lastClock = rotaryEncoder.GetClockInput()

    while isSelectingMenu:
        if rotaryEncoder.IsButtonPressed():
            isSelectingMenu = False
        else:
            currentClock = rotaryEncoder.GetClockInput()
            currentDirection = rotaryEncoder.GetDirectionInput()

            if currentClock != lastClock:
                if currentDirection != currentClock:
                    selectedMenu += 1  # Clockwise
                else:
                    selectedMenu -= 1  # Counter-clockwise

                lastClock = currentClock
                selectedMenu = Clamp(selectedMenu, 0, maxMenues)
                display.ShowMenuScanner(selectedMenu)

    return selectedMenu

def RunGameScanner():
    global display
    global rotaryEncoder
    global colorSendor

    isButtonPressed = False

    display.InstructionsScanner()

    while not isButtonPressed:
        isButtonPressed = rotaryEncoder.IsButtonPressed()

    colorName = colorSendor.GetColorName()
    display.ShowMenuScanner(1, colorName)

def RunGameMemory():
    global display
    global rotaryEncoder
    global colorSendor
    
    list = []
    list.append(AddEntry())

    maxPoints = 5
    currentPoints = 0
    isGameRunning = True
    didWin = False

    while isGameRunning:
        if currentPoints < maxPoints:
            print(list)

            i = 0
            while i < len(list):
                while not isButtonPressed:
                    isButtonPressed = rotaryEncoder.IsButtonPressed()

                rgb = colorSendor.GetColorRgb()

                buffer = 20
                r = rgb[0]-buffer <= list[i][0] <= rgb[0]+buffer
                g = rgb[1]-buffer <= list[i][1] <= rgb[1]+buffer
                b = rgb[2]-buffer <= list[i][2] <= rgb[2]+buffer

                if r and g and b:
                    i += 1
                    list.append(AddEntry())
                else:
                    display.ShowLog("Verlierer")
                    isGameRunning = False
                    i = len(list)

        else:
            display.ShowLog("Gewinner")
            isGameRunning = False
            didWin = True

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


display = OledDisplay()
rotaryEncoder = RotaryEncoder()
colorSendor = ColorSensor()

Main()