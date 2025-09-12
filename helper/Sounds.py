import json
import os
import random

import requests

from helper.Constants import Constants

c = Constants()


class Sounds:
    last_toast = ""
    fav_sounds_path = f"{c.pwd()}/assets/favorite-sounds.json"

    def search_sounds(self, query):
        response = requests.get(f"https://myinstants-api.vercel.app/search?q={query}").json()
        if response["status"] == "200":
            return response["data"]

        return []

    def add_favorite_sound(self, item):
        sounds = self.load_favorite_sounds()
        for sound in sounds:
            if sound["id"] == item["id"]:
                return 1

        with open(self.fav_sounds_path, "r+") as file:
            file_data = json.load(file)
            file_data.append(item)
            file.seek(0)
            json.dump(file_data, file, indent=4)

        return 0

    def delete_favorite_sound(self, item):
        with open(self.fav_sounds_path, "r+") as file:
            file_data = json.load(file)
            index = next(
                (i for i, station in enumerate(file_data) if station.get("id") == item.get("id")),
                None,
            )
            file_data.pop(index)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            file.truncate()

    def load_favorite_sounds(self):
        with open(self.fav_sounds_path) as file:
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
