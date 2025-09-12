import time

import alsaaudio as a
import vlc
from playsound3 import playsound

from helper.Constants import Constants
from helper.Sounds import Sounds
from helper.Stations import Stations

stations_helper = Stations()
c = Constants()
sounds = Sounds()


class Audio:
    audio = vlc.MediaPlayer("")
    toast_playing = False

    def __init__(self):
        self.init_sound()

    def init_sound(self):
        self.update_sound(30)

    def mixer(self):
        with open("/home/pi/mixers.txt", "w") as f:
            f.write(str(a.mixers()))
        return a.Mixer()

    def update_sound(self, value):
        if 0 <= value <= 100:
            self.mixer().setvolume(value)

    def mute(self):
        self.mixer().setmute(1)

    def unmute(self):
        self.mixer().setmute(0)

    def get_volume(self):
        return self.mixer().getvolume()[0]

    def toggle_mute(self):
        if self.is_mute():
            self.unmute()
            return False
        self.mute()
        return True

    def is_mute(self):
        return self.mixer().getmute()[0] == 1

    def play_src(self, src):
        try:
            self.pause()
        except Exception:
            print("Fehler beim abspielen des Radiosenders")
        Audio.audio = vlc.MediaPlayer(src)
        self.play()

    def play(self):
        Audio.audio.play()

    def pause(self):
        Audio.audio.stop()

    def play_sound(self, src):
        Audio.audio = vlc.MediaPlayer(src)
        self.play()

    def startup_sound(self):
        self.play_sound(f"{c.system_sound_path()}/startup.mp3")

    def shutdown_sound(self):
        self.pause()
        self.play_sound(f"{c.system_sound_path()}/shutdown.mp3")

    def bluetooth_connected(self):
        self.play_sound(f"{c.system_sound_path()}/bluetooth_connected.mp3")

    def bluetooth_disconnected(self):
        self.play_sound(f"{c.system_sound_path()}/bluetooth_disconnected.mp3")

    def play_toast(self):
        toast_src = sounds.get_random_toast()
        if not self.toast_playing:
            self.toast_playing = True
            self.pause()
            self.wait()
            self.toast = playsound(f"{c.toast_path()}/{toast_src}")
            self.wait()
            self.play()
            self.toast_playing = False

    def play_sound_board(self, src):
        if src.startswith("http"):
            playsound(src)
        else:
            playsound(f"{c.sound_path()}/{src}")

    def wait(self):
        time.sleep(0.5)
