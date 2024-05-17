import json
from System import System

s = System()

class Stations:
	def load_radio_stations(self):
		f = open(f"{s.pwd()}/radio-stations.json")
		data = json.load(f)
		f.close()
		return data
