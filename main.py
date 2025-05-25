from random import randrange
import RPi.GPIO as GPIO
from OledDisplay import OledDisplay
from RotaryEncoder import RotaryEncoder
from ColorSensor import ColorSensor

GPIO.setmode(GPIO.BCM)
#rotaryEncoder = RotaryEncoder()

def Main():
    RunMenuMain()

def RunMenuMain():
    DisplayMainMenu()

    while True:
        match MenuSelectionMain():
            case 1:
                RunMenuScanner()
            case 2:
                RunGameMemory()
            case _:
                return
            
def DisplayMainMenu():
    display = OledDisplay()
    display.ShowSelectedMenu("Menü")
    display.ShowMenuMain(1)
    display.Close()

def MenuSelectionMain():
    #global rotaryEncoder
    rotaryEncoder = RotaryEncoder()
    display = OledDisplay()
    
    selectedMenu = 1
    maxMenues = 2
    isSelectingMenu = True
    lastClock = rotaryEncoder.GetClockInput()
    
    display.ShowMenuMain(selectedMenu)

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
                display.ShowMenuMain(selectedMenu)

    rotaryEncoder.Close()
    display.Close()
    return selectedMenu

def RunMenuScanner():
    display = OledDisplay()
    display.ShowSelectedMenu("Scanner")
    display.ShowMenuScanner(1)

    match MenuSelectionScanner():
        case 1:
            RunGameScanner()
            display.Close()
        case _:
            display.Close()
            return

def MenuSelectionScanner():
    #global rotaryEncoder
    rotaryEncoder = RotaryEncoder()
    display = OledDisplay()
    
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

    rotaryEncoder.Close()
    display.Close()
    return selectedMenu

def RunGameScanner():
    WatilTilButtonPressed()

    colorName = GetColorName()

    DisplayShowMenuScanner(colorName)

def WatilTilButtonPressed():
    #global rotaryEncoder
    rotaryEncoder = RotaryEncoder()
    #display = OledDisplay()

    #display.InstructionsScanner()

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
    display.ShowMenuScanner(1, colorName)
    display.Close()

def RunGameMemory():
    #global rotaryEncoder
    rotaryEncoder = RotaryEncoder()
    
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
    

#rotaryEncoder = RotaryEncoder()

Main()

"""
File "/home/pat/Desktop/farberkennungsspiel/main.py", line 214, in <module>
    Main()
  File "/home/pat/Desktop/farberkennungsspiel/main.py", line 11, in Main
    RunMenuMain()
  File "/home/pat/Desktop/farberkennungsspiel/main.py", line 17, in RunMenuMain
    match MenuSelectionMain():
          ^^^^^^^^^^^^^^^^^^^
  File "/home/pat/Desktop/farberkennungsspiel/main.py", line 33, in MenuSelectionMain
    rotaryEncoder = RotaryEncoder()
                    ^^^^^^^^^^^^^^^
  File "/home/pat/Desktop/farberkennungsspiel/RotaryEncoder.py", line 10, in __init__
    GPIO.setup(self.clockPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 696, in setup
    _check(lgpio.gpio_claim_input(_chip, gpio, {
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/lgpio.py", line 755, in gpio_claim_input
    return _u2i(_lgpio._gpio_claim_input(handle&0xffff, lFlags, gpio))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/lgpio.py", line 458, in _u2i
    raise error(error_text(v))
lgpio.error: 'GPIO busy'
"""