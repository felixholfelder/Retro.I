import os

import RPi.GPIO as GPIO

# Hierbei handelt es sich um ein Überbleibsel aus Zeiten des Radio's des BSZ Wiesau, um bei offiziellen Veranstaltungen
# das Soundboard zu verstecken. Dabei muss dieses Skript in der main.py importiert werden.
# Um das Soundboard zu aktivieren, ...

GPIO.setmode(GPIO.BCM)

PIN = 21

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_state = GPIO.input(PIN)

if not input_state:
    os.environ["PARTY_MODE"] = "1"
else:
    os.system("unset PARTY_MODE")
