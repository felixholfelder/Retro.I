import os
import random

class Constants:
	def pwd(self):
		return "/home/pi/Desktop/Retro.I"
	
	def sound_path(self):
		return f"{self.pwd()}/assets/sounds"
	
	def get_button_img(self):
		ls = os.listdir(f"{self.pwd()}/assets/buttons")
		return f"{self.pwd()}/assets/buttons/{random.choice(ls)}"
