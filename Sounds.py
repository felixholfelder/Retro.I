import json
import os
import random
from Constants import Constants

c = Constants()

class Sounds:
	def load_sounds(self):
		f = open(f"{c.pwd()}/assets/sounds.json")
		data = json.load(f)
		f.close()
		return data
	
	def get_random_toast(self):
		directory = c.toast_path()
		try:
			files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
			return random.choice(files)
		except FileNotFoundError:
			return "Directory not found."
