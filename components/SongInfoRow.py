import flet as ft
from helper.Constants import Constants
from helper.RadioHelper import RadioHelper

constants = Constants()
radio_helper = RadioHelper()


class SongInfoRow:
    song_info_station = ft.Text("Kein Radiosender ausgewählt", weight=ft.FontWeight.BOLD)
    song_info_title = ft.Text("", expand=True)
    row = None

    def __init__(self, open_search_dialog):
        self.row = ft.Row([
            ft.Icon(ft.icons.MUSIC_NOTE),
            self.song_info_station,
            self.song_info_title,
            ft.TextButton("Sendersuche", icon=ft.icons.SEARCH, on_click=lambda e: open_search_dialog())
        ])

    def update(self):
        try:
            title = radio_helper.get_song_info(constants.current_radio_station["src"])

            if title != "":
                self.song_info_station.value = constants.current_radio_station["name"]
                self.song_info_title.value = title
            else:
                self.song_info_station.value = constants.current_radio_station["name"]
                self.song_info_title.value = ""
        except:
            pass

        self.song_info_station.update()
        self.song_info_title.update()

    def reset(self):
        constants.current_radio_station = {}
        self.song_info_station.value = "Kein Radiosender ausgewählt"
        self.song_info_title.value = ""

        self.song_info_station.update()
        self.song_info_title.update()

    def get(self): return self.row
