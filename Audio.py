import alsaaudio as a
import flet as ft
from Stations import Stations

stations_helper = Stations()
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
		print(src)
		audio.pause()
		audio.src = src
		audio.autoplay = True
		audio.play()
		audio.update()

	def init(self):
		return audio
