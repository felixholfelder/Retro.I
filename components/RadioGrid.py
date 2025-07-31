import flet as ft

from components.dialogs.StationDeleteDialog import StationDeleteDialog
from helper.Audio import Audio
from helper.Constants import Constants
from helper.PageState import PageState
from helper.RadioHelper import RadioHelper
from helper.Stations import Stations
from helper.Strip import Strip
from helper.SystemHelper import SystemHelper

constants = Constants()
stations_helper = Stations()
system_helper = SystemHelper()
audio_helper = Audio()
radio_helper = RadioHelper()


class RadioGrid(ft.GridView):
    delete_dialog: StationDeleteDialog = None
    on_strip_run_color = None
    on_theme_change_radio_station = None
    on_theme_stop_radio_station = None

    def __init__(self, on_strip_run_color, on_theme_change_radio_station, on_theme_stop_radio_station):
        super().__init__()
        self.delete_dialog = StationDeleteDialog(self.delete_station)
        self.on_strip_run_color = on_strip_run_color
        self.on_theme_change_radio_station = on_theme_change_radio_station
        self.on_theme_stop_radio_station = on_theme_stop_radio_station

        PageState.radio_grid = self.delete_dialog

        # Gridview attributes
        self.expand=True,
        self.runs_count=5,
        self.max_extent=150,
        self.child_aspect_ratio=1.0,
        self.spacing=20,
        self.run_spacing=50

    def open_delete_station_dialog(self, index):
        Constants.current_station_index_to_delete = index
        self.delete_dialog.open_dialog()

    def reload(self):
        self.controls.clear()
        Constants.indicator_refs = []

        for i, station in enumerate(stations_helper.load_radio_stations()):
            Constants.indicator_refs.append(ft.Ref[ft.Container]())
            self.controls.append(
                ft.Stack(
                    alignment=ft.alignment.center,
                    fit=ft.StackFit.EXPAND,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY_200,
                            on_click=lambda e, src=station, index=i: self.change_radio_station(src, self.on_theme_change_radio_station, index),
                            on_long_press=lambda e, index=i: self.open_delete_station_dialog(index),
                            border_radius=10,
                            content=self.get_content(station),
                            padding=10,
                        ),
                        ft.Container(
                            ref=Constants.indicator_refs[i],
                            on_click=lambda e: self.stop_radio_station(self.on_theme_stop_radio_station),
                            visible=False,
                            content=ft.Image(src=f"{constants.pwd()}/assets/party.gif", opacity=0.7)
                        )
                    ]
                )
            )
        self.update()

    def delete_station(self):
        stations_helper.delete_station(Constants.current_station_index_to_delete)
        self.reload()

    def change_radio_station(self, station, on_theme_change_radio_station=None, index=-1):
        color = station["color"]
        Constants.current_radio_station = station

        self.toggle_indicator(index)

        if on_theme_change_radio_station is not None:
            on_theme_change_radio_station(color)

        audio_helper.play_src(station["src"])

        self.on_strip_run_color(color)

    def stop_radio_station(self, on_theme_stop_radio_station):
        Constants.current_radio_station = {}
        self.toggle_indicator()
        audio_helper.pause()
        on_theme_stop_radio_station()

    def disable_indicator(self):
        for ref in Constants.indicator_refs:
            ref.current.visible = False

    def toggle_indicator(self, index=-1):
        self.disable_indicator()
        if index != -1:
            Constants.indicator_refs[index].current.visible = True

    def get_logo(self, station):
        return ft.Image(src=system_helper.get_img_path(station["logo"]), border_radius=ft.border_radius.all(4),
                        fit=ft.ImageFit.FIT_WIDTH)

    def get_text(self, station):
        return ft.Text(station["name"], text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)

    def get_content(self, station):        
        if station["logo"] != "":
            return self.get_logo(station)

        return self.get_text(station)
