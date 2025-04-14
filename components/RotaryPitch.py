from pyky040 import pyky040

from helper.Audio import Audio

audio_helper = Audio()

class RotaryPitch:
    last_turn = 0
    SW_PIN = 25 # PIN 22
    DT_PIN = 11 # PIN 23
    CLK_PIN = 8 # PIN 24

    def __init__(self):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_pitch(),
            dec_callback=lambda e: self.dec_pitch(),
            sw_callback=lambda: self.reset_pitch()
        )

    def inc_pitch(self):
        if self.last_turn == 1:
            # TODO - increase pitch
            pass
        self.last_turn = 1


    def dec_pitch(self):
        if self.last_turn == 0:
            # TODO - decrease pitch
            pass
        self.last_turn = 0


    def reset_pitch(self):
        # TODO - reset pitch to system default
        pass
