from pyky040 import pyky040

from helper.Audio import Audio

audio_helper = Audio()

class RotaryBassBoost:
    last_turn = 0
    SW_PIN = 4   # PIN 7
    DT_PIN = 14  # PIN 8
    CLK_PIN = 15 # PIN 10

    def __init__(self):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_bass_boost(),
            dec_callback=lambda e: self.dec_bass_boost(),
            sw_callback=lambda: self.reset_bass_boost()
        )

    def inc_bass_boost(self):
        if self.last_turn == 1:
            # TODO - increase bass-boost
            pass
        self.last_turn = 1


    def dec_bass_boost(self):
        if self.last_turn == 0:
            # TODO - decrease bass-boost
            pass
        self.last_turn = 0


    def reset_bass_boost(self):
        # TODO - reset bass-boost to system default
        pass
