import flet as ft
from helper.SystemHelper import System

system_helper = System()

class SettingsInfoDialog:
    dialog = None
    text = None

    def __init__(self):
        self.dialog = ft.AlertDialog(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                width=500,
                tight=True,
                controls=[
                    ft.Text(spans=[ft.TextSpan("CPU-Temperatur: "), self.text], size=20),
                    ft.Divider(),
                    ft.Text(f"Datum: {system_helper.get_curr_date()}", size=20),
                ]
            )
        )

    def open(self):
        self.text = system_helper.get_cpu_temp()
        self.dialog.open = True
        self.dialog.update()

    def get(self): return self.dialog
