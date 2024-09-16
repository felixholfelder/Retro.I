import flet as ft
from Constants import Constants
from Audio import Audio

c = Constants()
audio_helper = Audio()

class ToastCard:
	def get(page: ft.Page, i):
		return ft.Column(
                [
                    ft.Container(
                        alignment=ft.alignment.bottom_center,
                        on_click=lambda e, index=i: audio_helper.play_toast(),
                        height=130,
                        image_src=c.get_button_img(),
                    ),
                    ft.Container(
                        ft.Text("Zufälliger Trinkspruch", size=20, text_align=ft.TextAlign.CENTER),
                        width=300,
                    )
                ],
                width=300,
            )

ToastCard.get = staticmethod(ToastCard.get)
