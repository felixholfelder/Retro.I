import json
import os
import random

import requests

from helper.Constants import Constants

c = Constants()

class Sounds:
	last_toast = ""

	def search_sounds(self, query):
		response = requests.get(f"https://myinstants-api.vercel.app/search?q={query}")
		if response.status == 200:
			return response.data

		return []

	def load_favorite_sounds(self):
		with open(f"{c.pwd()}/assets/favorite_sounds.json") as file:
			data = json.load(file)
			return data

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
