import flet as ft

from helper.System import System
from helper.WifiHelper import WifiHelper

system_helper = System()
wifi_helper = WifiHelper()


class WifiDialog:
    loading = ft.Text("Netzwerke werden geladen...")
    listview = ft.ListView(spacing=10, padding=20, expand=True)

    taskbar = None
    dialog = None
    connection_dialog = None

    def __init__(self, connection_dialog):
        self.connection_dialog = connection_dialog

        self.dialog = ft.AlertDialog(
            content=ft.Column(
                width=500,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[self.loading, self.listview]
            )
        )

    def open(self):
        self.loading.visible = True
        self.loading.update()

        self.listview.controls = []
        self.listview.update()

        self.dialog.open = True
        self.dialog.update()

        curr_ssid = wifi_helper.get_current_ssid()
        networks = wifi_helper.get_networks()

        for n in networks:
            ico = ft.Icon(ft.icons.DONE)
            btn = ft.TextButton(
                content=ft.Container(content=ft.Row(controls=[ico, ft.Text(n)])),
                on_click=lambda e, name=n: self.connection_dialog.open(name),
            )

            if (curr_ssid != n):
                ico.visible = False

            self.listview.controls.append(btn)

        self.listview.update()

        self.loading.visible = False
        self.loading.update()

    def close(self):
        self.dialog.open = False
        self.dialog.update()

    def get(self): return self.dialog
