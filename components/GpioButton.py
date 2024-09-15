import RPi.GPIO as GPIO


class GpioButton:
    def __init__(self, pin, callback):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(10, GPIO.RISING, callback=callback)  # Setup event on pin 10 rising edge
