import alsaaudio as a
import flet as ft
from Stations import Stations
from Constants import Constants
import pyglet

stations_helper = Stations()
c = Constants()
audio = ft.Audio(src=stations_helper.load_radio_stations()[0]["src"], autoplay=False)

class Audio:	
	def mixer(self):
		return a.Mixer()

	def update_sound(self, value):
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

	def play(self, src):
		self.pause()
		audio.src = src
		audio.autoplay = True
		audio.play()
		audio.update()

	def pause(self):
		audio.pause()

	def init(self):
		return audio
	
	def startup_sound(self):
		self.play_sound("startup.mp3")
	
	def shutdown_sound(self):
		self.play_sound("shutdown.mp3")
	
	def play_sound(self, src):
		sound = pyglet.media.load(f"{c.sound_path()}/{src}")
		sound.play()
