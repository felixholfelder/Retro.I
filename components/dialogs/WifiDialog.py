import flet as ft

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from helper.PageState import PageState
from helper.SystemHelper import SystemHelper
from helper.WifiHelper import WifiHelper

system_helper = SystemHelper()
wifi_helper = WifiHelper()


class WifiDialog(ft.AlertDialog):
    loading = ft.ProgressRing(visible=False)
    not_found = ft.Text("Keine Netzwerke gefunden", visible=False)
    listview = ft.ListView(spacing=10, padding=20, expand=True, visible=False)

    connection_dialog: WifiConnectionDialog = None

    def __init__(self, connection_dialog: WifiConnectionDialog):
        super().__init__()

        self.connection_dialog = connection_dialog

        self.content = ft.Column([
            ft.Text("Verfügbare Netzwerke:", size=20, weight=ft.FontWeight.BOLD),
            ft.Column(
                width=500,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.loading,
                    self.not_found,
                    self.listview,
                ]
            )
        ])

    def open_dialog(self):
        self.listview.visible = False
        self.listview.update()

        self.not_found.visible = False
        self.not_found.update()

        self.loading.visible = True
        self.loading.update()

        self.listview.controls = []
        self.listview.update()

        self.open = True
        self.update()

        curr_ssid = wifi_helper.get_current_ssid()
        networks = wifi_helper.get_networks()

        for n in networks:
            ico = ft.Icon(ft.icons.DONE, size=28, visible=False)
            btn = ft.TextButton(
                content=ft.Container(content=ft.Row(controls=[ico, ft.Text(n, size=16)])),
                on_click=lambda e, name=n: self.connection_dialog.open_dialog(name),
            )

            if curr_ssid == n:
                ico.visible = True

            self.listview.controls.append(btn)

        self.loading.visible = False
        self.loading.update()

        if len(networks) == 0:
            self.not_found.visible = True
            self.not_found.update()

        self.listview.visible = True
        self.listview.update()

    def close(self):
        self.open = False
        self.update()
