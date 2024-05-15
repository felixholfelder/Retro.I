import json


class Stations:
	def load_radio_stations(self):
		f = open('radio-stations.json')
		data = json.load(f)
		f.close()
		return data
