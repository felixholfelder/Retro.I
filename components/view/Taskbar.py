import flet as ft

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from helper.Audio import Audio
from helper.WifiHelper import WifiHelper
from helper.BluetoothHelper import BluetoothHelper

audio_helper = Audio()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()

class Taskbar:
    taskbar = None
    
    wifi_connection_dialog: WifiConnectionDialog = None
    wifi_dialog: WifiDialog = None

    ico_wifi = ft.IconButton(icon=ft.icons.WIFI, icon_size=25, icon_color=ft.colors.GREEN)
    ico_bluetooth = ft.Icon(name=ft.icons.BLUETOOTH, size=25)
    ico_volume = ft.Icon(name=ft.icons.VOLUME_UP_ROUNDED, size=25, color=ft.colors.BLACK)
    txt_volume = ft.Text("", size=18)

    def __init__(self):
        self.taskbar = ft.AppBar(
            leading=ft.Row([
                self.ico_volume,
                self.txt_volume
            ],
                spacing=10
            ),
            title=ft.Text("Retro.I"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            toolbar_height=40,
            actions=[self.ico_wifi, self.ico_bluetooth],
        )

        self.wifi_connection_dialog = WifiConnectionDialog(self.update)
        self.wifi_dialog = WifiDialog(self.wifi_connection_dialog)
        self.ico_wifi.on_click = lambda e: self.wifi_dialog.open()

    def update(self):
        self.update_volume()
        self.update_wifi()
        self.update_bluetooth()

    def update_volume(self):
        self.ico_volume.name = ft.icons.VOLUME_UP_ROUNDED if not audio_helper.is_mute() else ft.icons.VOLUME_OFF_ROUNDED,
        self.ico_volume.color = ft.colors.BLACK if not audio_helper.is_mute() else ft.colors.RED
        self.ico_volume.update()
        self.txt_volume.value = f"{audio_helper.get_volume()}%" if not audio_helper.is_mute() else ""
        self.txt_volume.update()

    def update_wifi(self):
        self.ico_wifi.name = ft.icons.WIFI if wifi_helper.is_connected() else ft.icons.WIFI_OFF_ROUNDED
        self.ico_wifi.color = ft.colors.GREEN if wifi_helper.is_connected() else ft.colors.BLACK
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
            self.ico_bluetooth.color = ft.colors.BLACK

        if bluetooth_helper.is_connected():
            self.ico_bluetooth.name = ft.icons.BLUETOOTH_CONNECTED_ROUNDED
            self.ico_bluetooth.color = ft.colors.GREEN

        self.ico_bluetooth.update()


    def get(self): return self.taskbar
    def get_wifi_dialog(self): return self.wifi_dialog
    def get_wifi_connection_dialog(self): return self.wifi_connection_dialog
