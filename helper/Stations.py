import json
from helper.Constants import Constants

c = Constants()

class Stations:
	def load_radio_stations(self):
		f = open(f"{c.pwd()}/assets/radio-stations.json")
		data = json.load(f)
		f.close()
		return data

	def add_station(self, station):
		with open(f"{c.pwd()}/assets/radio-stations.json",'r+') as file:
			# First we load existing data into a dict.
			file_data = json.load(file)
			# Join new_data with file_data inside emp_details
			file_data.append(station)
			# Sets file's current position at offset.
			file.seek(0)
			# convert back to json.
			json.dump(file_data, file, indent = 4)
