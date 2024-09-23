import flet as ft

from components.SoundCard import SoundCard
from components.ToastCard import ToastCard
from helper.Sounds import Sounds

sounds = Sounds()

class SoundboardTab:
    tab = None

    def __init__(self):
        soundboard_grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            spacing=80,
            run_spacing=50
        )

        # Card for toast (drinking)
        soundboard_grid.controls.append(ToastCard().get())

        for i in range(len(sounds.load_sounds())):
            sound = sounds.load_sounds()[i]
            soundboard_grid.controls.append(SoundCard.get(sound["src"], sound["name"], i))

        self.tab = ft.Container(
            content=ft.Column([ft.Row([soundboard_grid])]),
            visible=False,
            margin=ft.margin.only(right=75, bottom=75),
        )

    def update(self):
        self.tab.update()

    def get(self): return self.tab