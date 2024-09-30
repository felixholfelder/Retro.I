import flet as ft
from helper.Strip import Strip

strip = Strip()

class SettingsLedDialog:
    dialog = None

    def __init__(self):
        self.dialog = ft.AlertDialog(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                width=500,
                tight=True,
                controls=[
                    ft.Switch(
                        "LED-Streifen ausschalten",
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
        )

    def open(self):
        self.dialog.open = True
        self.dialog.update()

    def get(self): return self.dialog