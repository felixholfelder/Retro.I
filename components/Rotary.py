import threading
from pyky040 import pyky040

from components.view.Taskbar import Taskbar
from helper.Audio import Audio
from helper.Strip import Strip

audio_helper = Audio()

class Rotary:
    last_turn = 1
    SW_PIN = 5
    DT_PIN = 6
    CLK_PIN = 13
    VOLUME_STEP = 4

    taskbar: Taskbar = None
    strip: Strip = None

    def __init__(self, taskbar: Taskbar, strip: Strip):
        self.taskbar = taskbar
        self.strip = strip

        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            step=self.VOLUME_STEP,
            inc_callback=lambda e: self.inc_sound(),
            dec_callback=lambda e: self.dec_sound(),
            sw_callback=lambda: self.toggle_mute()
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_sound(self):
        if self.last_turn == 1:
            value = audio_helper.get_volume() + self.VOLUME_STEP
            if 0 <= value <= 100:
                self.update_sound(value)
        self.last_turn = 1


    def dec_sound(self):
        if self.last_turn == 0:
            value = audio_helper.get_volume() - self.VOLUME_STEP
            if 0 <= value <= 100:
                self.update_sound(value)
        self.last_turn = 0


    def toggle_mute(self):
        is_mute = audio_helper.toggle_mute()
        self.strip.toggle_mute(is_mute)
        self.taskbar.update()

    def update_sound(self, value):
        if not audio_helper.is_mute():
            audio_helper.update_sound(value)
            self.strip.update_sound_strip(value)
            self.taskbar.update()
