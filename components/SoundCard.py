import flet as ft
from helper.Constants import Constants
from helper.Audio import Audio
from helper.Sounds import Sounds

c = Constants()
audio_helper = Audio()
sounds = Sounds()

class SoundCard:
	def get(self, source, name, i):
		return ft.Column(
                [
                    ft.Container(
                        alignment=ft.alignment.bottom_center,
                        on_click=lambda e, index=i, src=source: audio_helper.play_sound(src),
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
