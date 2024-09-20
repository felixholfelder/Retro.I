import threading
from pyky040 import pyky040
from helper.Audio import Audio

audio_helper = Audio()

class Rotary:
    last_turn = 1
    SW_PIN = 5
    DT_PIN = 6
    CLK_PIN = 13
    VOLUME_STEP = 4

    def __init__(self, taskbar, strip):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            step=self.VOLUME_STEP,
            inc_callback=lambda e: self.inc_sound(taskbar, strip),
            dec_callback=lambda e: self.dec_sound(taskbar, strip),
            sw_callback=lambda: self.toggle_mute(taskbar, strip)
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_sound(self, taskbar, strip):
        if self.last_turn == 1:
            value = audio_helper.get_volume() + self.VOLUME_STEP
            if 0 <= value <= 100:
                self.update_sound(value, taskbar, strip)
        self.last_turn = 1


    def dec_sound(self, taskbar, strip):
        if self.last_turn == 0:
            value = audio_helper.get_volume() - self.VOLUME_STEP
            if 0 <= value <= 100:
                self.update_sound(value, taskbar, strip)
        self.last_turn = 0


    def toggle_mute(self, strip, taskbar):
        is_mute = audio_helper.toggle_mute()
        strip.toggle_mute(is_mute)
        taskbar.update()

    def update_sound(self, value, taskbar, strip):
        if not audio_helper.is_mute():
            audio_helper.update_sound(value)
            strip.update_sound_strip(value)
            taskbar.update()
