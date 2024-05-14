import alsaaudio as audio
import flet as ft

from main import load_radio_stations


class Audio:
	def mixer(self):
		return audio.Mixer()

	def update_sound(self, value):
		if value >= 0 and value <= 100:
			self.mixer().setvolume(value)

	def mute(self):
		self.mixer().setmute(1)

	def unmute(self):
		self.mixer().setmute(0)
	
	def get_volume(self):
		print(self.mixer().getvolume()[0])
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
		audio.pause()
		audio.src = src
		audio.autoplay = True
		audio.play()
		audio.update()

	def init(self):
		return ft.Audio(
			src=load_radio_stations()[0]["src"], autoplay=False
		)
