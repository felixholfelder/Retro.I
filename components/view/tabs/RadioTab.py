import flet as ft

from components.RadioGrid import RadioGrid
from components.SongInfoRow import SongInfoRow
from helper.Strip import Strip


class RadioTab:
    tab = None

    radio_grid: RadioGrid = None
    song_info_row: SongInfoRow = None

    def __init__(self, strip: Strip, theme):
        self.radio_grid = RadioGrid(strip, theme)
        self.song_info_row = SongInfoRow(self.radio_grid)

        self.tab = ft.Container(
            content=ft.Column([
                self.song_info_row.get(),
                ft.Row([self.radio_grid.get()])
            ]),
        )

    def update(self):
        self.song_info_row.reload()
        self.tab.update()

    def show(self):
        self.tab.visible = True
        self.tab.update()

    def hide(self):
        self.tab.visible = False
        self.song_info_row.reset()
        self.tab.update()

    def get(self): return self.tab
    def get_grid(self): return self.radio_grid
    def get_song_info(self): return self.song_info_row
    def get_search_dialog(self): return self.song_info_row.get_search_dialog()
    def get_station_add_dialog(self): return self.song_info_row.get_station_add_dialog()
