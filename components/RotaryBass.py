import threading

from pyky040 import pyky040

from components.view.Taskbar import Taskbar
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects

audio_helper = Audio()
audio_effects = AudioEffects()


class RotaryBass:
    COUNTER = 0
    BASS_STEP = 2
    CLK_PIN = 4  # PIN 7
    DT_PIN = 14  # PIN 8

    taskbar = None

    def __init__(self, taskbar: Taskbar):
        self.taskbar = taskbar
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_bass_boost(),
            dec_callback=lambda e: self.dec_bass_boost()
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_bass_boost(self):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_bass_value() + self.BASS_STEP
            self.update(value)
        self.COUNTER += 1

    def dec_bass_boost(self):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_bass_value() - self.BASS_STEP
            self.update(value)
        self.COUNTER -= 1

    def update(self, value):
        audio_effects.update_bass(value)
        self.taskbar.update()
