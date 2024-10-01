import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)

PIN = 21

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_state = GPIO.input(PIN)

if input_state == False:
    os.environ["PARTY_MODE"] = "1"
else:
    os.system("unset PARTY_MODE")
