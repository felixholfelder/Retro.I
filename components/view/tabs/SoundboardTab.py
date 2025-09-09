import flet as ft

from components.SoundCard import SoundCard
from components.SoundboardSearchBar import SoundboardSearchBar
from components.ToastCard import ToastCard
from components.dialogs.SoundDeleteDialog import SoundDeleteDialog
from helper.PageState import PageState
from helper.Sounds import Sounds

sounds = Sounds()

class SoundboardTab(ft.Column):
    soundboard_grid = None
    sound_delete_dialog = None

    def __init__(self):
        super().__init__()

        self.sound_delete_dialog = SoundDeleteDialog()
        PageState.page.add(self.sound_delete_dialog)

        self.soundboard_grid = ft.GridView(
            [],
            expand=True,
            runs_count=5,
            run_spacing=50,
            max_extent=150,
            spacing=80,
            padding=ft.padding.only(bottom=80),
        )
        self.reload()

        self.soundboard_search_bar = SoundboardSearchBar(self.on_add_favorite_sound)

        self.expand=True
        self.visible=False
        self.controls=[
            self.soundboard_search_bar,
            self.soundboard_grid,
        ]

    def reload(self):
        controls=[ToastCard()]

        for i in range(len(sounds.load_favorite_sounds())):
            sound = sounds.load_favorite_sounds()[i]
            controls.append(SoundCard(sound, self.open_delete_dialog))

        self.soundboard_grid.controls = controls

    def open_delete_dialog(self, sound):
        self.sound_delete_dialog.open_dialog(
            submit_callback=lambda s=sound: self.on_delete_favorite_sound(s)
        )

    def on_add_favorite_sound(self, sound):
        result = sounds.add_favorite_sound(sound)
        if result == 1:
            return

        self.soundboard_grid.controls.append(SoundCard(sound, self.open_delete_dialog))
        self.soundboard_grid.update()

    def on_delete_favorite_sound(self, sound):
        sounds.delete_favorite_sound(sound)
        self.reload()
        self.soundboard_grid.update()
        self.sound_delete_dialog.close()

    def show(self):
        self.visible = True
        self.reload()
        self.soundboard_grid.update()
        self.update()

    def hide(self):
        self.visible = False
        self.update()
