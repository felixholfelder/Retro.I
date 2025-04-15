import threading

from pyky040 import pyky040

from helper.Audio import Audio
from helper.AudioEffects import AudioEffects

audio_helper = Audio()
audio_effects = AudioEffects()


class RotaryBassBoost:
    last_turn = 0
    BASS_STEP = 1
    SW_PIN = 4  # PIN 7
    DT_PIN = 14  # PIN 8
    CLK_PIN = 15  # PIN 10

    def __init__(self):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_bass_boost(),
            dec_callback=lambda e: self.dec_bass_boost()
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_bass_boost(self):
        if self.last_turn == 1:
            value = audio_effects.get_bass_value() + self.BASS_STEP
            audio_effects.update_bass(value)
        self.last_turn = 1

    def dec_bass_boost(self):
        if self.last_turn == 0:
            value = audio_effects.get_bass_value() - self.BASS_STEP
            audio_effects.update_bass(value)
        self.last_turn = 0
