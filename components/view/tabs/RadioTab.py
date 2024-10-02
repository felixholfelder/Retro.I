import flet as ft

from components.RadioGrid import RadioGrid
from components.dialogs.RadioSearchDialog import RadioSearchDialog
from helper.Strip import Strip


class RadioTab:
    tab = None

    radio_grid: RadioGrid = None

    def __init__(self, strip: Strip, theme):
        self.radio_grid = RadioGrid(strip, theme)

        self.tab = ft.Container(
            content=ft.Column([
                ft.Row([self.radio_grid.get()])
            ]),
            margin=ft.margin.only(right=60)
        )

    def update(self):
        self.tab.update()

    def show(self):
        self.tab.visible = True
        self.update()

    def hide(self):
        self.tab.visible = False
        self.song_info_row.reset()
        self.tab.update()

    def get(self): return self.tab
    def get_grid(self): return self.radio_grid
