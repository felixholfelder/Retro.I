import flet as ft

from helper.System import System

system_helper = System()


class SettingsShutdownDialog:
    dialog = None

    def __init__(self):
        self.dialog = ft.AlertDialog(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                width=500,
                tight=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=75,
                        controls=[
                            ft.Column(
                                [
                                    ft.IconButton(ft.icons.POWER_OFF, icon_size=75,
                                                  on_click=system_helper.shutdown_system),
                                    ft.Text("Ausschalten", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=16))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column(
                                [
                                    ft.IconButton(ft.icons.REPLAY, icon_size=75, on_click=system_helper.restart_system),
                                    ft.Text("Neustarten", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=16))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER),
                        ]
                    )
                ]
            )
        )

    def open(self):
        self.dialog.open = True
        self.dialog.update()

    def get(self): return self.dialog
