import flet as ft

from components.RadioGrid import RadioGrid
from components.dialogs.DuplicateDialog import DuplicateDialog
from helper.Constants import Constants
from helper.Stations import Stations

constants = Constants()
stations_helper = Stations()

class StationAddDialog:
    dialog = None
    station = {"name": ""}

    text = ft.Text(station["name"])
    on_play = None

    radio_grid: RadioGrid = None

    duplicate_dialog = DuplicateDialog()

    def __init__(self, radio_grid: RadioGrid):
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
        self.close()
        self.radio_grid.change_radio_station(self.station)

    def add_to_list(self):
        stations_list = stations_helper.load_radio_stations()
        found = False
        for el in stations_list:
            if el["name"] == self.station["name"]:
                found = True
                self.duplicate_dialog.open(self.station["name"])
                break

        if not found:
            stations_helper.add_station(self.station)
            self.radio_grid.reload()

        self.close()


    def close(self):
        self.dialog.open = False
        self.dialog.update()


    def open(self, element):
        self.station = element
        self.text.value = element["name"]
        self.dialog.open = True
        self.dialog.update()

    def get(self): return self.dialog
    def get_duplicate_dialog(self): return self.duplicate_dialog
