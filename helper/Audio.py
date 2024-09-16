import time
import alsaaudio as a
import flet as ft
from Stations import Stations
from Constants import Constants
from playsound import playsound
from Sounds import Sounds

stations_helper = Stations()
c = Constants()
audio = ft.Audio(src=stations_helper.load_radio_stations()[0]["src"], autoplay=False)
sounds = Sounds()

class Audio:
	def __init__(self):
		self.init_sound()

	def init_sound(self):
		self.update_sound(20)

	def mixer(self):
		return a.Mixer()

	def update_sound(self, value):
		if value >= 0 and value <= 100:
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
		self.pause()
		audio.release()
		audio.src = src
		audio.autoplay = True
		self.play()

	def play(self):
		audio.play()

	def pause(self):
		audio.pause()

	def init(self):
		return audio
	
	def startup_sound(self):
		self.play_sound("startup.mp3")
	
	def shutdown_sound(self):
		self.play_sound("shutdown.mp3")
	
	def play_sound(self, src):
		playsound(f"{c.sound_path()}/{src}")
	
	def play_toast(self):
		toast_src = sounds.get_random_toast()
		self.pause()
		self.wait()
		playsound(f"{c.toast_path()}/{toast_src}")
		self.wait()
		self.play()

	def wait(self):
		time.sleep(0.5)
