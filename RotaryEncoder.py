import RPi.GPIO as GPIO
from time import sleep
from OledDisplay import OledDisplay

class RotaryEncoder():
    def __init__(self):
        self.clockPin = 17
        self.directionPin = 18
        self.buttonPin = 27

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clockPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.directionPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def GetClockInput(self):
        input = GPIO.input(self.clockPin)
        sleep(0.002)
        return input
    
    def GetDirectionInput(self):
        input = GPIO.input(self.directionPin)
        sleep(0.002)
        return input

    def IsButtonPressed(self):
        input = GPIO.input(self.buttonPin) == GPIO.LOW
        sleep(0.002)
        return input
