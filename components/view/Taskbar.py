import flet as ft

from components.dialogs.WifiConnectDialog import WifiConnectDialog
from components.dialogs.WifiDialog import WifiDialog
from helper.Audio import Audio
from helper.WifiHelper import WifiHelper
from helper.BluetoothHelper import BluetoothHelper

audio_helper = Audio()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()


class Taskbar:
    taskbar = None
    ico_wifi = ft.IconButton(
        icon=ft.icons.WIFI if wifi_helper.is_connected() else ft.icons.WIFI_OFF_ROUNDED,
        icon_size=25,
        icon_color=ft.colors.GREEN if wifi_helper.is_connected() else ft.colors.BLACK,
    )
    ico_bluetooth = ft.Icon(name=ft.icons.BLUETOOTH, size=25)

    volume_icon = ft.Icon(
        name=ft.icons.VOLUME_UP_ROUNDED if not audio_helper.is_mute() else ft.icons.VOLUME_OFF_ROUNDED,
        size=25,
        color=ft.colors.BLACK
    )
    volume_text = ft.Text(f"{audio_helper.get_volume()}%" if not audio_helper.is_mute() else "", size=18)

    wifi_connection_dialog = None
    wifi_dialog = None

    def __init__(self):
        self.taskbar = ft.AppBar(
            leading=ft.Row([
                self.volume_icon,
                self.volume_text
            ],
                spacing=10
            ),
            title=ft.Text("Retro.I"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            toolbar_height=40,
            actions=[self.ico_wifi, self.ico_bluetooth],
        )

        self.wifi_connection_dialog = WifiConnectDialog(self.taskbar)
        self.wifi_dialog = WifiDialog(self.wifi_connection_dialog)
        self.ico_wifi.on_click = lambda e: self.wifi_dialog.open()

    def update(self):
        self.update_volume()
        self.update_wifi()
        self.update_bluetooth()

    def update_volume(self):
        self.volume_icon.update()
        self.volume_text.update()

    def update_wifi(self):
        self.ico_wifi.update()

    def update_bluetooth(self):
        if bluetooth_helper.is_bluetooth_on():
            self.ico_bluetooth.name = ft.icons.BLUETOOTH_ROUNDED
            self.ico_bluetooth.color = ft.colors.BLACK
            if bluetooth_helper.is_discovery_on():
                self.ico_bluetooth.color = ft.colors.GREEN
            else:
                self.ico_bluetooth.color = ft.colors.BLACK

        else:
            self.ico_bluetooth.name = ft.icons.BLUETOOTH_DISABLED_ROUNDED

        if bluetooth_helper.get_device_name():
            self.ico_bluetooth.name = ft.icons.BLUETOOTH_CONNECTED_ROUNDED
            self.ico_bluetooth.color = ft.colors.GREEN

        self.ico_bluetooth.update()


    def get(self): return self.taskbar
    def get_dialogs(self): return [self.wifi_dialog.get(), self.wifi_connection_dialog.get()]
