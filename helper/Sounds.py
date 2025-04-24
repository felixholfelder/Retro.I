import json
import os
import random

from helper.Constants import Constants

c = Constants()

class Sounds:
	last_toast = ""
	
	def load_sounds(self):
		directory = c.sound_path()
		files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
		return files

	def load_toasts(self):
		directory = c.toast_path()
		files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		return files

	def get_random_toast(self):
		try:
			ran = random.choice(self.load_toasts())
			while self.last_toast == ran:
				ran = random.choice(self.load_toasts())
			
			self.last_toast = ran
			return ran
		except FileNotFoundError:
			pass
