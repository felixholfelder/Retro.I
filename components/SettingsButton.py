import flet as ft


class SettingsButton:
    def get(self, icon, text, callback):
        return ft.TextButton(
            height=100,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon),
                    ft.Text(f"{text}", style=ft.TextStyle(size=20))
                ]
            ),
            on_click=callback
        )
