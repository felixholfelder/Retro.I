import flet as ft

from components.SoundCard import SoundCard
from components.ToastCard import ToastCard
from helper.Sounds import Sounds

sounds = Sounds()

class SoundboardTab(ft.Column):
    soundboard_grid = None

    def __init__(self):
        super().__init__()

        self.soundboard_grid = ft.GridView(
            [ToastCard()],
            expand=True,
            runs_count=5,
            run_spacing=50,
            max_extent=150,
            spacing=80,
            padding=ft.padding.only(bottom=80),
        )
        for i in range(len(sounds.load_favorite_sounds())):
            sound = sounds.load_favorite_sounds()[i]
            self.soundboard_grid.controls.append(SoundCard(sound))

        self.expand=True
        self.visible=False
        self.controls=[self.soundboard_grid]

    def show(self):
        self.visible = True
        self.update()

    def hide(self):
        self.visible = False
        self.update()
