import RPi.GPIO as GPIO
from time import sleep


CLK = 17
DT = 18
SW = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
last_clk = GPIO.input(CLK)

try:
    while True:
        current_clk = GPIO.input(CLK)
        current_dt = GPIO.input(DT)

        if current_clk != last_clk:
            if current_dt != current_clk:
                counter += 1
            else:
                counter -= 1
            print(f"Counter: {counter}")

        last_clk = current_clk

        if GPIO.input(SW) == GPIO.LOW:
            print("Button pressed!")
            sleep(0.3)

        sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()