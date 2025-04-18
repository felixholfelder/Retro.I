import flet as ft

from helper.Audio import Audio
from helper.Constants import Constants
from helper.Sounds import Sounds

c = Constants()
audio_helper = Audio()
sounds = Sounds()


class SoundCard:
    def get(self, file_name):
        name = file_name.replace("_", " ").replace(".mp3", "").title()
        return ft.Column(
            [
                ft.Container(
                    alignment=ft.alignment.bottom_center,
                    on_click=lambda e, src=file_name: audio_helper.play_sound_board(src),
                    height=130,
                    image_src=c.get_button_img(),
                ),
                ft.Container(
                    ft.Text(name, size=20, text_align=ft.TextAlign.CENTER),
                    width=300,
                )
            ],
            width=300,
        )
