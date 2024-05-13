import flet as ft


class Background(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.expand = True

    def build(self) -> ft.Container:
        return ft.Container(
            bgcolor=ft.colors.GREEN_200,
            expand=True,
        )
