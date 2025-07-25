import flet as ft

from helper.PageState import PageState
from helper.Strip import Strip
from helper.SystemHelper import SystemHelper

strip = Strip()
system_helper = SystemHelper()

class SettingsBrightnessDialog:
    dialog = None

    def __init__(self):
        self.dialog = ft.AlertDialog(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                width=500,
                tight=True,
                controls=[
                    ft.Row([
                        ft.Text("Helligkeit", style=ft.TextStyle(size=20)),
                        ft.Slider(
                            min=10, max=100, divisions=10, label="{value}%", on_change=self.slider_changed
                        ),
                    ])
                ]
            )
        )
        PageState.page.add(self.dialog)

    def slider_changed(self, e):
        system_helper.change_screen_brightness(e.control.value)

    def open(self):
        self.dialog.open = True
        self.dialog.update()
