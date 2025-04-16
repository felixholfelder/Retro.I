import threading

from pyky040 import pyky040

from components.view.Taskbar import Taskbar
from helper.AudioEffects import AudioEffects

audio_effects = AudioEffects()


class RotaryPitch:
    LAST_TURN = 0
    PITCH_STEP = 1
    SW_PIN = 25  # PIN 22
    DT_PIN = 11  # PIN 23
    CLK_PIN = 8  # PIN 24

    taskbar = None

    def __init__(self, taskbar: Taskbar):
        self.taskbar = taskbar
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            step=self.PITCH_STEP,
            inc_callback=lambda e: self.inc_pitch(),
            dec_callback=lambda e: self.dec_pitch(),
            sw_callback=lambda: self.pass_sw()
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_pitch(self):
        if self.LAST_TURN == 1:
            print("INC PITCH")
            value = audio_effects.get_pitch_value() + self.PITCH_STEP
            if -12 <= value <= 12:
                self.update(value)

            if value > 12:
                self.update(12)
        self.LAST_TURN = 1

    def dec_pitch(self):
        if self.LAST_TURN == 0:
            print("DEC PITCH")
            value = audio_effects.get_pitch_value() - self.PITCH_STEP
            if -12 <= value <= 12:
                self.update(value)

            if value < -12:
                self.update(-12)
        self.LAST_TURN = 0

    def pass_sw(self):
        pass

    def update(self, value):
        audio_effects.update_pitch(value)
        self.taskbar.update()
