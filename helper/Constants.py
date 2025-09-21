import os
import random
from pathlib import Path


class Constants:
    current_radio_station = {}
    current_station_index_to_delete = None
    indicator_refs = []

    def pwd(self) -> str:
        retroi_dir = os.environ.get("RETROI_DIR")
        if retroi_dir:
            return retroi_dir

        return str(Path(__file__).resolve().parent.parent)

    def sound_path(self):
        return f"{self.pwd()}/assets/sounds"

    def system_sound_path(self):
        return f"{self.pwd()}/assets/system_sounds"

    def toast_path(self):
        return f"{self.pwd()}/assets/toasts"

    def get_button_img(self):
        ls = os.listdir(f"{self.pwd()}/assets/buttons")
        return f"{self.pwd()}/assets/buttons/{random.choice(ls)}"
