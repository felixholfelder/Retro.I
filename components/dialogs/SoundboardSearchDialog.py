import flet as ft

from helper.Audio import Audio
from helper.Constants import Constants
from helper.Sounds import Sounds
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
sounds_helper = Sounds()
constants = Constants()
audio = Audio()


class SoundboardSearchDialog(ft.AlertDialog):
    text = ft.Text("")

    loading = ft.ProgressRing(visible=False)
    not_found_text = ft.Text("Keine Sounds gefunden!", visible=False)
    listview = ft.ListView(spacing=10, expand=True, visible=False)
    search_textfield = ft.TextField(
        label="Sounds",
        expand=True,
        on_focus=lambda e: system_helper.open_keyboard(),
        on_blur=lambda e: system_helper.close_keyboard()
    )

    def __init__(self, soundboard_grid: ft.GridView):
        super().__init__()

        self.soundboard_grid = soundboard_grid

        self.content = ft.Column(
            width=600,
            expand=True,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                        self.search_textfield,
                        ft.FilledButton("Suchen", on_click=lambda e: self.search_sounds()),
                    ],
                    spacing=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Column(
                    controls=[
                        self.loading,
                        self.not_found_text,
                        self.listview
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )

    def open_dialog(self):
        self.open = True
        self.update()

    def close(self):
        self.open = False
        self.update()

    def search_sounds(self):
        self.listview.visible = False
        self.listview.update()

        self.loading.visible = True
        self.loading.update()

        query = self.search_textfield.value
        sounds = sounds_helper.search_sounds(query)

        self.loading.visible = False
        self.loading.update()

        if len(sounds) == 0:
            self.not_found_text.visible = True
        else:
            self.not_found_text.visible = False

        self.not_found_text.update()

        self.listview.controls = []
        for el in sounds:
            img = ft.Image(f"{constants.pwd()}/assets/buttons/SB_green.png", fit=ft.ImageFit.SCALE_DOWN, border_radius=ft.border_radius.all(10), width=50, height=50)
            element = ft.Container(
                content=ft.Row(
                    controls=[
                        img,
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(el["title"], weight=ft.FontWeight.BOLD, expand=True),
                                ft.SubmenuButton(
                                    content=ft.IconButton(icon=ft.icons.MORE_VERT, icon_size=40),
                                    controls=[
                                        ft.MenuItemButton(
                                            content=ft.Text("Zu Favoriten hinzufügen"),
                                            leading=ft.Icon(ft.icons.STAR),
                                            on_click=lambda e, item=el: self.on_favorite_add(item),
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ]
                ),
                on_click=lambda e, item=el: self.play_sound(item)
            )

        self.listview.controls.append(element)

        self.listview.visible = True
        self.listview.update()

    def play_sound(self, item):
        audio.play_sound_board(item["mp3"])

    def on_favorite_add(self, item):
        sounds_helper.add_favorite_sound(item)
        self.soundboard_grid.update()