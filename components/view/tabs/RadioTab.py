import flet as ft

from components.RadioGrid import RadioGrid
from components.SongInfoRow import SongInfoRow
from components.view.Theme import Theme
from helper.Strip import Strip


class RadioTab:
    tab = None

    radio_grid: RadioGrid = None
    song_info_row: SongInfoRow = None

    def __init__(self, strip: Strip, theme: Theme):
        self.radio_grid = RadioGrid(strip, theme)
        self.song_info_row = SongInfoRow(self.radio_grid)

        self.tab = ft.Container(
            content=ft.Column([
                self.song_info_row.get(),
                ft.Row([self.radio_grid])
            ]),
            margin=ft.margin.only(right=75)
        )

    def update(self):
        self.song_info_row.update()
        self.tab.update()

    def get(self): return self.tab
    def get_grid(self): return self.radio_grid
    def get_song_info(self): return self.song_info_row