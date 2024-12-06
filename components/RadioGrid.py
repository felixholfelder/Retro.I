import flet as ft

from components.dialogs.StationDeleteDialog import StationDeleteDialog
from helper.Audio import Audio
from helper.Constants import Constants
from helper.RadioHelper import RadioHelper
from helper.Stations import Stations
from helper.Strip import Strip
from helper.SystemHelper import System

constants = Constants()
stations_helper = Stations()
system_helper = System()
audio_helper = Audio()
radio_helper = RadioHelper()


class RadioGrid:
    grid = None
    delete_dialog: StationDeleteDialog = None

    strip: Strip = None
    theme = None

    page = None

    def __init__(self, strip: Strip, theme, page: ft.Page):
        self.delete_dialog = StationDeleteDialog(self.delete_station)
        self.strip = strip
        self.theme = theme
        self.page = page

        self.grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=20,
            run_spacing=50
        )

    def open_delete_station_dialog(self, index):
        Constants.current_station_index_to_delete = index
        self.delete_dialog.open()

    def reload(self):
        self.grid.controls = []
        Constants.indicator_refs = []

        for i, station in enumerate(stations_helper.load_radio_stations()):
            Constants.indicator_refs.append(ft.Ref[ft.Image]())
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
                            content=self.get_content(station),
                            padding=10,
                        ),
                        ft.Image(ref=Constants.indicator_refs[i], src=f"{constants.pwd()}/assets/party.gif",
                                 opacity=0.7,
                                 visible=False)
                    ]
                )
            )
        self.page.update()

    def delete_station(self):
        stations_helper.delete_station(Constants.current_station_index_to_delete)
        self.reload()

    def change_radio_station(self, station, index=-1):
        color = station["color"]
        Constants.current_radio_station = station

        self.toggle_indicator(index)
        self.theme.update(color)
        audio_helper.play_src(station["src"])

        self.strip.run(color)

    def disable_indicator(self):
        for ref in Constants.indicator_refs:
            ref.current.visible = False

    def toggle_indicator(self, index):
        self.disable_indicator()
        if index != -1:
            Constants.indicator_refs[index].current.visible = True

    def get_logo(self, station):
        return ft.Image(src=system_helper.get_img_path(station["logo"]), border_radius=ft.border_radius.all(4),
                        fit=ft.ImageFit.FIT_WIDTH)

    def get_text(self, station):
        return ft.Text(station["name"], text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),

    def get_content(self, station):
        if station["logo"] != "":
            return self.get_logo(station)

        return self.get_text(station)

    def get(self): return self.grid
    def get_delete_dialog(self): return self.delete_dialog
