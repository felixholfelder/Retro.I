import flet as ft

from helper.Strip import Strip

strip = Strip()


class SettingsLedDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch(
                    "LED-Streifen ausschalten",
                    label_position=ft.LabelPosition.LEFT,
                    label_style=ft.TextStyle(size=20),
                    on_change=lambda e: strip.toggle_strip(),
                    value=strip.is_strip_active()
                ),
                ft.Divider(),
                ft.Row([
                    ft.Text("Helligkeit", style=ft.TextStyle(size=20)),
                    ft.Slider(
                        on_change=strip.change_brightness,
                        min=0,
                        max=100,
                        value=strip.get_curr_brightness(),
                        expand=True
                    )
                ])
            ]
        )

    def open_dialog(self):
        self.open = True
        self.update()
