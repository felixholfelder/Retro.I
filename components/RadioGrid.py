import flet as ft

from components.dialogs.StationDeleteDialog import StationDeleteDialog
from helper.Constants import Constants
from helper.RadioHelper import RadioHelper
from helper.Stations import Stations
from helper.System import System
from helper.Audio import Audio

constants = Constants()
stations_helper = Stations()
system_helper = System()
audio_helper = Audio()
radio_helper = RadioHelper()

class RadioGrid:
    grid = None
    delete_dialog = None

    strip = None
    theme = None

    def __init__(self, strip, theme):
        self.delete_dialog = StationDeleteDialog(self.delete_station)
        self.strip = strip
        self.theme = theme

        self.grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=20,
            run_spacing=50
        )

    def open_delete_station_dialog(self, index):
        constants.current_station_index_to_delete = index
        self.delete_dialog.open()


    def reload(self):
        self.grid.controls = []
        constants.indicator_refs = []

        for i, station in enumerate(stations_helper.load_radio_stations()):
            constants.indicator_refs.append(ft.Ref[ft.Image]())
            self.grid.controls.append(
                ft.Stack(
                    alignment=ft.MainAxisAlignment.END,
                    fit=ft.StackFit.EXPAND,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY_200,
                            on_click=lambda e, src=station, index=i: self.change_radio_station(src, index),
                            on_long_press=lambda e, index=i: self.open_delete_station_dialog(index),
                            border_radius=10,
                            # TODO - expand???
                            content=ft.Image(src=system_helper.get_img_path(station["logo"]),
                                             border_radius=ft.border_radius.all(4), fit=ft.ImageFit.FIT_WIDTH) if station[
                                                                                                                      "logo"] != "" else ft.Text(
                                station["name"], text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                            padding=10,
                        ),
                        ft.Image(ref=constants.indicator_refs[i], src=f"{constants.pwd()}/assets/party.gif", opacity=0.7,
                                 visible=False)
                    ]
                )
            )

        self.grid.update()

    def delete_station(self):
        stations_helper.delete_station(constants.current_station_index_to_delete)
        self.reload()

    def change_radio_station(self, src, index=-1):
        station = radio_helper.get_stations_by_name(src["name"])
        color = station[1]["color"]

        self.toggle_indicator(index)
        self.theme = ft.Theme(color_scheme_seed=color)
        audio_helper.play_src(station[1]["src"])
        self.theme.update()

        self.strip.run(color)


    def disable_indicator(self):
        for ref in constants.indicator_refs:
            ref.current.visible = False


    def toggle_indicator(self, index):
        self.disable_indicator()
        if index != -1:
            constants.indicator_refs[index].current.visible = True

    def get(self): return self.grid
    def get_delete_dialog(self): return self.delete_dialog