import flet as ft
from PIL.ImageOps import expand

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from helper.PageState import PageState
from helper.SystemHelper import SystemHelper
from helper.WifiHelper import WifiHelper

system_helper = SystemHelper()
wifi_helper = WifiHelper()


class WifiDialog:
    dialog = None

    loading = ft.ProgressRing(visible=False)
    not_found = ft.Text("Keine Netzwerke gefunden", visible=False)
    listview = ft.ListView(spacing=10, padding=20, expand=True, visible=False)

    connection_dialog: WifiConnectionDialog = None

    def __init__(self, connection_dialog: WifiConnectionDialog):
        self.connection_dialog = connection_dialog

        self.dialog = ft.AlertDialog(
            content=ft.Column(
                width=500,
                height=500,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.loading,
                    self.not_found,
                    self.listview,
                ],
            ),
        )
        PageState.page.add(self.dialog)

    def open(self):
        self.listview.visible = False
        self.listview.update()
        
        self.not_found.visible = False
        self.not_found.update()

        self.loading.visible = True
        self.loading.update()

        self.listview.controls = []
        self.listview.update()

        self.dialog.open = True
        self.dialog.update()

        curr_ssid = wifi_helper.get_current_ssid()
        networks = wifi_helper.get_networks()

        for n in networks:
            ico = ft.Icon(ft.icons.DONE, visible=False)
            btn = ft.TextButton(
                content=ft.Container(content=ft.Row(controls=[ico, ft.Text(n)])),
                on_click=lambda e, name=n: self.connection_dialog.open(name),
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
        self.dialog.open = False
        self.dialog.update()
