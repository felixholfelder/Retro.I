import flet as ft

class SettingsCreditsDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.content = ft.Column(
            width=500,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ListView(
                    controls=[
                        ft.Text("Retro.i", weight=ft.FontWeight.BOLD, size=28),
                        ft.Divider(),
                        ft.Text("Klasse: FWI1 2023/2024", weight=ft.FontWeight.BOLD, size=20),
                        ft.Text("Felix Holfelder", size=20),
                        ft.Text("Dominik Schelter", size=20),
                        ft.Text("Johannes Lehner", size=20),
                        ft.Text("Yannick Grübl", size=20),
                        ft.Divider(),
                        ft.Text("Besonderen Dank an:", weight=ft.FontWeight.BOLD, size=22),
                        ft.Text("Goldschmiede und Uhren Gruhle", size=20),
                        ft.Text("Felix Diermeier", size=20),
                        ft.Text("Thomas Holfelder", size=20),
                    ]
                )
            ]
        )

    def open_dialog(self):
        self.open = True
        self.update()
