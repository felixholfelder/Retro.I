from gpiozero import LED, Button

class GpioButton:
    button = None
    callback = None

    def __init__(self, pin, callback):
        self.button = Button(pin)
        self.callback = callback
        self.deactivate()

    def on_pressed(self):
        self.deactivate()
        self.callback()
        self.activate()

    def activate(self):
        self.button.when_pressed = lambda e: self.on_pressed()

    def deactivate(self):
        self.button.when_pressed = None
