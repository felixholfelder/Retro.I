import json
from Constants import Constants

c = Constants()

class Sounds:
	def load_sounds(self):
		f = open(f"{c.pwd()}/assets/sounds.json")
		data = json.load(f)
		f.close()
		return data
