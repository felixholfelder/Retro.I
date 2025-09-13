import csv
import os
import random


class Constants:
    current_radio_station = {}
    current_station_index_to_delete = None
    indicator_refs = []

    def pwd(self):
        with open("../settings/working-directory-settings.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar=" ")
            for row in reader:
                return row

        return "/home/pi/Documents/Retro.I"

    def sound_path(self):
        return f"{self.pwd()}/assets/sounds"

    def system_sound_path(self):
        return f"{self.pwd()}/assets/system_sounds"

    def toast_path(self):
        return f"{self.pwd()}/assets/toasts"

    def get_button_img(self):
        ls = os.listdir(f"{self.pwd()}/assets/buttons")
        return f"{self.pwd()}/assets/buttons/{random.choice(ls)}"
