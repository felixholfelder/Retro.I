import RPi.GPIO as GPIO
import time
import flet as ft
import alsaaudio as audio
from pyky040 import pyky040
import threading

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 5

# Pin numbers on Raspberry Pi
CLK_PIN = 21
DT_PIN = 16
SW_PIN = 15
LED_PIN = 8

DIRECTION_CW = 0
DIRECTION_CCW = 1

counter = 0
CLK_state = 0
prev_CLK_state = 0

button_pressed = False
prev_button_state = GPIO.HIGH

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


def getCurrentVolume():
    return audio.Mixer().getvolume()


def updateSound(value):
    print("Update " + str(value))
    mixer = audio.Mixer()
    mixer.setvolume(int(value))
    #slider.value = int(value)
    #p.update()


def clk_listener(val):
    global counter, MIN_VOLUME
    print("Rechts")
    if counter-5 >= MIN_VOLUME:
        counter -= 5
        updateSound(counter)

    
def dt_listener(val):
    global counter, MAX_VOLUME
    print("Links")
    if counter+5 <= MAX_VOLUME:
        counter += 5
        updateSound(counter)


def sw_listener(val):
    if button_state == True:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
rotary.setup(scale_min=MIN_VOLUME, scale_max=MAX_VOLUME, step=VOLUME_STEP, chg_callback=updateSound)
my_thread = threading.Thread(target=rotary.watch)
my_thread.start()


button = ft.FilledButton(text="0")
slider = ft.Slider(min=MIN_VOLUME, max=MAX_VOLUME, divisions=20, label="{value}%", value=getCurrentVolume(), on_change=lambda event: updateSound(event.control.value))


def main(p: ft.Page):
    p.title = "Retro.I"
    p.bgcolor = "green100"

    p.add(button)
    p.add(slider)

    p.update()


ft.app(main)
