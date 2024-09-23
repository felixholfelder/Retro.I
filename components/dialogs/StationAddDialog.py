import flet as ft

from components.dialogs.DuplicateDialog import DuplicateDialog
from helper.Constants import Constants
from helper.Stations import Stations

constants = Constants()
stations_helper = Stations()

class StationAddDialog:
    dialog = None
    text = ft.Text(f'{constants.current_station_to_add["name"]}')
    on_submit = None
    on_play = None

    radio_grid = None

    duplicate_dialog = DuplicateDialog()

    def __init__(self, on_play, radio_grid):
        self.on_play = on_play
        self.radio_grid = radio_grid

        self.dialog = ft.AlertDialog(
            content=ft.Column(
                width=500,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            title=self.text,
            actions=[
                ft.FilledButton("Abspielen", on_click=lambda e: self.play()),
                ft.FilledButton("Zu Liste hinzufügen", on_click=lambda e: self.add_to_list())
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def play(self):
        self.on_play()
        self.close()

    def add_to_list(self):
        station = constants.current_station_to_add
        stations_list = stations_helper.load_radio_stations()
        found = False
        for el in stations_list:
            if el["name"] == station["name"]:
                found = True
                self.duplicate_dialog.open(constants.current_station_to_add["name"])
                break

        if not found:
            stations_helper.add_station(station)
            self.radio_grid.update()
        self.close()


    def close(self):
        self.dialog.open = False
        self.dialog.update()


    def open(self, element):
        constants.current_station_to_add = element
        self.text.value = element["name"]
        self.dialog.open = True
        self.dialog.update()

    def get(self): return [self.dialog, self.duplicate_dialog]
