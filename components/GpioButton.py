from gpiozero import LED, Button

class GpioButton:
    def __init__(self, pin, callback):
        button = Button(pin)
        button.when_pressed = callback
