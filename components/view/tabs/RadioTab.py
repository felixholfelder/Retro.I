import flet as ft

from components.RadioGrid import RadioGrid
from components.SongInfoRow import SongInfoRow


class RadioTab:
    tab = None

    radio_grid = None
    song_info_row = None

    def __init__(self, strip, theme):
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