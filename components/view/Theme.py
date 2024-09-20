import flet as ft

class Theme:
    theme = None

    def __init__(self):
        self.theme = ft.Theme(
            color_scheme_seed='green',
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                },
                thumb_visibility=True,
                thumb_color={
                    ft.MaterialState.HOVERED: ft.colors.GREY_500,
                    ft.MaterialState.DEFAULT: ft.colors.GREY_400,
                },
                thickness=40,
                radius=20,
            )
        )

    def update(self, color):
        self.theme.color_scheme_seed = color
        self.theme.update()

    def get(self): return self.theme