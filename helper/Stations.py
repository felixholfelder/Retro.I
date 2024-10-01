import json
from helper.Constants import Constants
from helper.ColorHelper import ColorHelper

c = Constants()
color_helper = ColorHelper()

class Stations:
    def load_radio_stations(self):
        with open(f"{c.pwd()}/assets/radio-stations.json") as file:
            data = json.load(file)
            return data

    def add_station(self, station):
        if station["name"] != "":
            station["color"] = color_helper.extract_color(station["logo"])

        with open(f"{c.pwd()}/assets/radio-stations.json", "r+") as file:
            file_data = json.load(file)
            file_data.append(station)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def delete_station(self, index):
        with open(f"{c.pwd()}/assets/radio-stations.json", "r+") as file:
            file_data = json.load(file)
            file_data.pop(index)

        with open(f"{c.pwd()}/assets/radio-stations.json", "w") as file:
            file.write(json.dumps(file_data, sort_keys=True, indent=4, separators=(',', ': ')))
