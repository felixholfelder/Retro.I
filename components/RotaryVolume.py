import threading

from pyky040 import pyky040

from helper.Audio import Audio

audio_helper = Audio()


class RotaryVolume:
    COUNTER = 0
    VOLUME_STEP = 6
    SW_PIN = 13  # PIN 33
    DT_PIN = 12  # PIN 32
    CLK_PIN = 6  # PIN 31

    def __init__(self, on_taskbar_update, on_strip_toggle_mute, on_strip_update_sound):
        rotary = pyky040.Encoder(CLK=self.CLK_PIN, DT=self.DT_PIN, SW=self.SW_PIN)
        rotary.setup(
            step=self.VOLUME_STEP,
            inc_callback=lambda e: self.inc_sound(on_taskbar_update, on_strip_update_sound),
            dec_callback=lambda e: self.dec_sound(on_taskbar_update, on_strip_update_sound),
            sw_callback=lambda: self.toggle_mute(on_taskbar_update, on_strip_toggle_mute),
        )
        rotary_thread = threading.Thread(target=rotary.watch)
        rotary_thread.start()

    def inc_sound(self, on_taskbar_update, on_strip_update_sound):
        if self.COUNTER % 2 == 0:
            value = audio_helper.get_volume() + self.VOLUME_STEP
            if 0 <= value <= 100:
                self.update(value, on_taskbar_update, on_strip_update_sound)

            if value > 100:
                self.update(100, on_taskbar_update, on_strip_update_sound)
        self.COUNTER += 1

    def dec_sound(self, on_taskbar_update, on_strip_update_sound):
        if self.COUNTER % 2 == 0:
            value = audio_helper.get_volume() - self.VOLUME_STEP
            if 0 <= value <= 100:
                self.update(value, on_taskbar_update, on_strip_update_sound)

            if value < 0:
                self.update(0, on_taskbar_update, on_strip_update_sound)
        self.COUNTER -= 1

    def toggle_mute(self, on_taskbar_update, on_strip_toggle_mute):
        is_mute = audio_helper.toggle_mute()
        on_strip_toggle_mute(is_mute)
        on_taskbar_update()

    def update(self, value, on_taskbar_update, on_strip_update_sound):
        if not audio_helper.is_mute():
            audio_helper.update_sound(value)
            on_strip_update_sound(value)
            on_taskbar_update()
