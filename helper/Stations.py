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
        with open(f"{c.pwd()}/assets/radio-stations.json", "r+") as file:
            file_data = json.load(file)
            file_data.append(station)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def delete_station(self, index):
        with open(f"{c.pwd()}/assets/radio-stations.json", "r+") as file:
            file_data = json.load(file)
            file_data.pop(index)

        open("./assets/radio-stations.json", "w").write(
            json.dumps(file_data, sort_keys=True, indent=4, separators=(',', ': '))
        )
