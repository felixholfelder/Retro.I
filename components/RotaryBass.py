import threading

from pyky040 import pyky040

from helper.Audio import Audio
from helper.AudioEffects import AudioEffects

audio_helper = Audio()
audio_effects = AudioEffects()


class RotaryBass:
    COUNTER = 0
    BASS_STEP = 2
    CLK_PIN = 4  # PIN 7
    DT_PIN = 14  # PIN 8

    def __init__(self, on_taskbar_update):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_bass_boost(on_taskbar_update),
            dec_callback=lambda e: self.dec_bass_boost(on_taskbar_update)
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_bass_boost(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_bass_value() + self.BASS_STEP
            self.update(value, on_taskbar_update)
        self.COUNTER += 1

    def dec_bass_boost(self, on_taskbar_update):
        if self.COUNTER % 2 == 0:
            value = audio_effects.get_bass_value() - self.BASS_STEP
            self.update(value, on_taskbar_update)
        self.COUNTER -= 1

    def sw_callback(self):
        pass

    def update(self, value, on_taskbar_update):
        audio_effects.update_bass(value)
        on_taskbar_update()
