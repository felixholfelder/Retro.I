from pyky040 import pyky040

from helper.Audio import Audio
from helper.AudioEffects import AudioEffects

audio_helper = Audio()
audio_effects = AudioEffects()

class RotaryPitch:
    LAST_TURN = 0
    PITCH_STEP = 1
    SW_PIN = 25 # PIN 22
    DT_PIN = 11 # PIN 23
    CLK_PIN = 8 # PIN 24

    def __init__(self):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            inc_callback=lambda e: self.inc_pitch(),
            dec_callback=lambda e: self.dec_pitch()
        )

    def inc_pitch(self):
        if self.LAST_TURN == 1:
            value = audio_effects.get_pitch_value() + self.PITCH_STEP
            if -12 <= value <= 12:
                audio_effects.update_pitch(value)

            if value > 12:
                audio_effects.update_pitch(12)
        self.LAST_TURN = 1


    def dec_pitch(self):
        if self.LAST_TURN == 0:
            value = audio_effects.get_pitch_value() - self.PITCH_STEP
            if -12 <= value <= 12:
                audio_effects.update_pitch(value)

            if value < -12:
                audio_effects.update_pitch(-12)
        self.LAST_TURN = 0
