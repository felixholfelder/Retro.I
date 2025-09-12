import flet as ft

from components.RadioGrid import RadioGrid
from components.SongInfoRow import SongInfoRow


class RadioTab(ft.Column):
    radio_grid: RadioGrid = None
    song_info_row: SongInfoRow = None

    def __init__(
        self,
        on_strip_run_color,
        on_theme_change_radio_station,
        on_theme_stop_radio_station,
    ):
        super().__init__()

        self.radio_grid = RadioGrid(
            on_strip_run_color,
            on_theme_change_radio_station,
            on_theme_stop_radio_station,
        )
        self.song_info_row = SongInfoRow(self.radio_grid)

        self.controls = [
            self.song_info_row,
            self.radio_grid,
        ]
        self.expand = True

    def update(self):
        self.song_info_row.reload()
        super().update()

    def show(self):
        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.song_info_row.reset()
        self.update()

    def get_grid(self):
        return self.radio_grid

    def get_song_info(self):
        return self.song_info_row
