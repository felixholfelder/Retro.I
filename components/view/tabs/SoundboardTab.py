import flet as ft

from components.SoundCard import SoundCard
from components.ToastCard import ToastCard
from helper.Sounds import Sounds

sounds = Sounds()

class SoundboardTab:
    tab = None
    soundboard_grid = None

    def __init__(self):
        self.soundboard_grid = ft.GridView(
            [ToastCard().get()],
            expand=True,
            runs_count=5,
            max_extent=150,
            spacing=80,
            run_spacing=50
        )
        for i in range(len(sounds.load_sounds())):
            sound = sounds.load_sounds()[i]
            self.soundboard_grid.controls.append(SoundCard().get(sound))

        self.tab = ft.Column(
            [
                ft.Text("Soundboard", size=24, weight=ft.FontWeight.BOLD),
                self.soundboard_grid
            ],
            expand=True,
            visible=False
        )

    def update(self):
        self.tab.update()

    def show(self):
        self.tab.visible = True
        self.update()

    def hide(self):
        self.tab.visible = False
        self.update()

    def get(self): return self.tab
