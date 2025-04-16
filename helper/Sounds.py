import json
import os
import random

from helper.Constants import Constants

c = Constants()

class Sounds:
	def load_sounds(self):
		directory = c.sound_path()
		files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		return files

	def load_toasts(self):
		directory = c.toast_path()
		files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		return files

	def get_random_toast(self):
		try:
			return random.choice(self.load_toasts())
		except FileNotFoundError:
			pass
