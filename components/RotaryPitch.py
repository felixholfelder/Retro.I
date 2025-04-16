import threading

from pyky040 import pyky040

from components.view.Taskbar import Taskbar
from helper.AudioEffects import AudioEffects

audio_effects = AudioEffects()


class RotaryPitch:
    COUNTER = 0
    PITCH_STEP = 1
    CLK_PIN = 11  # PIN 23
    DT_PIN = 8  # PIN 24

    taskbar = None

    def __init__(self, taskbar: Taskbar):
        self.taskbar = taskbar
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_pitch(),
            dec_callback=lambda e: self.dec_pitch()
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_pitch(self):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_pitch_value() + self.PITCH_STEP
            if -12 <= value <= 12:
                self.update(value)

            if value > 12:
                self.update(12)
        self.COUNTER += 1

    def dec_pitch(self):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_pitch_value() - self.PITCH_STEP
            if -12 <= value <= 12:
                self.update(value)

            if value < -12:
                self.update(-12)
        self.COUNTER -= 1

    def update(self, value):
        audio_effects.update_pitch(value)
        self.taskbar.update()
