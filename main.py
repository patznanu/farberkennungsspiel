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
                print("FEHLT")
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

def Clamp(number, min, max):
    if (number < min):
        return max
    
    if number > max:
        return min
    
    return number


display = OledDisplay()
rotaryEncoder = RotaryEncoder()
colorSendor = ColorSensor()

Main()