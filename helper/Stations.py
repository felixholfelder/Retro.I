import json
from Constants import Constants

c = Constants()

class Stations:
	def load_radio_stations(self):
		f = open(f"{c.pwd()}/assets/radio-stations.json")
		data = json.load(f)
		f.close()
		return data
