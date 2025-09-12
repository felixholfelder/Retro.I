import flet as ft


class SettingsButton(ft.Container):
    def __init__(self, icon, text, callback):
        super().__init__()

        self.alignment = ft.alignment.center
        self.on_click = callback
        self.border_radius = 10
        self.padding = 10
        self.ink = True
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icon, size=36),
                ft.Text(f"{text}", style=ft.TextStyle(size=20)),
            ],
        )
