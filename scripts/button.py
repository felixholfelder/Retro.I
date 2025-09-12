import os

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

PIN = 21

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_state = GPIO.input(PIN)

input_state = False  # Enable soundboard

if not input_state:
    os.environ["PARTY_MODE"] = "1"
else:
    os.system("unset PARTY_MODE")
