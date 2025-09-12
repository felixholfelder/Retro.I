import flet as ft

from helper.SystemHelper import SystemHelper
from helper.WifiHelper import WifiHelper

system_helper = SystemHelper()
wifi_helper = WifiHelper()


class WifiConnectionDialog(ft.AlertDialog):
    ssid = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    password = ft.TextField(
        password=True,
        autofocus=True,
        on_focus=lambda e: system_helper.open_keyboard(),
        on_blur=lambda e: system_helper.close_keyboard(),
    )
    btn_connect = ft.FilledButton("Verbinden", style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)))

    def __init__(self, on_connect):
        super().__init__()

        self.btn_connect.on_click = lambda e: self.connect(on_connect)

        self.actions = [self.btn_connect]
        self.content = ft.Column(
            width=400,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.ssid,
                ft.Row([ft.Text("Passwort:", size=18), self.password]),
            ],
        )

    def open_dialog(self, name):
        self.ssid.value = name
        self.ssid.update()
        self.open = True
        self.update()

    def close(self):
        self.open = False
        self.update()

    def connect(self, on_connect):
        self.btn_connect.disabled = True
        self.btn_connect.text = "Wird verbunden..."
        self.btn_connect.update()
        on_connect()

        wifi_helper.connect_to_wifi(self.ssid.value, self.password.value)

        self.password.value = ""

        self.close()
        self.btn_connect.disabled = False
        self.btn_connect.text = "Verbinden"
        on_connect()
