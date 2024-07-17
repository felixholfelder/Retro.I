import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

PIN = 21

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_state = GPIO.input(PIN)

if input_state == False:
    os.environ["SAFE_MODE"] = "1"
else:
    os.system("unset SAFE_MODE")


if os.getenv("SAFE_MODE") is not None:
    print("SET")
else:
    print("NOT_SET")
