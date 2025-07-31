import flet as ft

from helper.Strip import Strip
from helper.SystemHelper import SystemHelper

strip = Strip()
system_helper = SystemHelper()


class SettingsBrightnessDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Helligkeit", style=ft.TextStyle(size=20)),
                        ft.Slider(
                            expand=True,
                            min=10,
                            max=100,
                            divisions=19,
                            label="{value}%",
                            value=system_helper.get_curr_brightness(),
                            on_change=self.slider_changed,
                        ),
                    ]
                )
            ]
        )

    def slider_changed(self, e):
        system_helper.change_screen_brightness(e.control.value)

    def open_dialog(self):
        self.open = True
        self.update()
