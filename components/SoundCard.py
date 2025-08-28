import flet as ft

from helper.Audio import Audio
from helper.Constants import Constants
from helper.Sounds import Sounds

c = Constants()
audio_helper = Audio()
sounds = Sounds()


class SoundCard(ft.Container):
    def __init__(self, sound):
        super().__init__()
        self.content = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        alignment=ft.alignment.bottom_center,
                        on_click=lambda e, src=sound["mp3"]: audio_helper.play_sound_board(src),
                        #on_long_press=lambda e, sound=sound: self.delete_favorite_sound(sound),
                        content=ft.Image(
                            src=c.get_button_img(),
                            border_radius=ft.border_radius.all(4),
                            fit=ft.ImageFit.FIT_WIDTH),
                        height=130,
                    ),
                    ft.Container(
                        ft.Text(sound ["title"], size=20, text_align=ft.TextAlign.CENTER),
                        width=300,
                    )
                ]
            )
        )
