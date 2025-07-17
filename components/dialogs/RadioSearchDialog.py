import flet as ft

from components.RadioGrid import RadioGrid
from components.dialogs.StationAddDialog import StationAddDialog
from helper.Constants import Constants
from helper.PageState import PageState
from helper.RadioHelper import RadioHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
radio_helper = RadioHelper()
constants = Constants()


class RadioSearchDialog:
    text = ft.Text("")
    dialog = None

    loading = ft.ProgressRing(visible=False)
    not_found_text = ft.Text("Kein Radiosender gefunden!", visible=False)
    listview = ft.ListView(spacing=10, expand=True, visible=False)
    search_textfield = ft.TextField(
        label="Radiosender",
        expand=True,
        on_focus=lambda e: system_helper.open_keyboard(),
        on_blur=lambda e: system_helper.close_keyboard()
    )

    station_add_dialog: StationAddDialog = None

    def __init__(self, radio_grid: RadioGrid):
        self.station_add_dialog = StationAddDialog(radio_grid)

        self.dialog = ft.AlertDialog(
            content=ft.Column(
                width=600,
                expand=True,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        [
                            self.search_textfield,
                            ft.FilledButton("Suchen", on_click=lambda e: self.search_stations()),
                        ],
                        spacing=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Column(
                        controls=[
                            self.loading,
                            self.not_found_text,
                            self.listview
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )
        PageState.page.add(self.dialog)

    def open(self):
        self.dialog.open = True
        self.dialog.update()

    def close(self):
        self.dialog.open = False
        self.dialog.update()

    def search_stations(self):
        self.listview.visible = False
        self.listview.update()

        self.loading.visible = True
        self.loading.update()

        name = self.search_textfield.value
        stations = radio_helper.get_stations_by_name(name)

        self.loading.visible = False
        self.loading.update()

        if len(stations) == 0:
            self.not_found_text.visible = True
        else:
            self.not_found_text.visible = False

        self.not_found_text.update()

        self.listview.controls = []
        for el in stations:
            img = ft.Container(ft.Icon(ft.icons.MUSIC_NOTE), width=60, height=60)
            if el["logo"] != "":
                img = ft.Image(el["logo"], fit=ft.ImageFit.SCALE_DOWN, border_radius=ft.border_radius.all(10), width=50, height=50)

            element = ft.Container(
                content=ft.Row(
                    controls=[
                        img,
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(el["name"], weight=ft.FontWeight.BOLD),
                                ft.Text(el["src"])
                            ]
                        )
                    ]
                ),
                on_click=lambda e, item=el: self.station_add_dialog.open(item)
            )

            self.listview.controls.append(element)

        self.listview.visible = True
        self.listview.update()
