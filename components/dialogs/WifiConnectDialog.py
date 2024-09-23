import flet as ft

from helper.System import System
from helper.WifiHelper import WifiHelper

system_helper = System()
wifi_helper = WifiHelper()


class WifiConnectDialog:
    ssid = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    password = ft.TextField(password=True, autofocus=True,
                            on_focus=lambda e: system_helper.open_keyboard(),
                            on_blur=lambda e: system_helper.close_keyboard())
    btn_connect = ft.FilledButton("Verbinden")

    taskbar = None
    dialog = None

    def __init__(self, taskbar):
        self.btn_connect.on_click = lambda e: self.connect(taskbar)

        self.dialog = ft.AlertDialog(
            content=ft.Column(
                width=400,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.ssid,
                    ft.Row([ft.Text("Passwort:", size=18), self.password]),
                ]
            ),
            actions=[self.btn_connect]
        )

    def open(self, name):
        self.ssid.value = name
        self.ssid.update()
        self.dialog.open = True
        self.dialog.update()

    def close(self):
        self.dialog.open = False
        self.dialog.update()

    def connect(self, taskbar):
        self.btn_connect.disabled = True
        self.btn_connect.text = "Wird verbunden..."
        taskbar.update()
        p.update()

        wifi_helper.connect_to_wifi(self.ssid.value, self.password.value)

        self.password.value = ""

        self.close()
        self.btn_connect.disabled = False
        self.btn_connect.text = "Verbinden"
        taskbar.update()

    def get(self): return self.dialog
