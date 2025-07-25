import flet as ft


class SettingsButton:
    def get(self, icon, text, callback):
        return ft.Container(
            alignment=ft.alignment.center,
            on_click=callback,
            border_radius=10,
            padding=10,
            ink=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, size=36),
                    ft.Text(f"{text}", style=ft.TextStyle(size=20))
                ]
            ),
        )
