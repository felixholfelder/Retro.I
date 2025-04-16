import flet as ft

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from components.view.TaskbarBass import TaskbarBass
from components.view.TaskbarPitch import TaskbarPitch
from components.view.TaskbarVolume import TaskbarVolume
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

    taskbar_volume = TaskbarVolume()
    taskbar_bass = TaskbarBass()
    taskbar_pitch = TaskbarPitch()

    def __init__(self):
        self.taskbar = ft.AppBar(
            leading=ft.Row([
                self.taskbar_volume.get(),
                self.taskbar_bass.get(),
                self.taskbar_pitch.get(),
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
        self.taskbar_volume.update()
        self.update_wifi()
        self.update_bluetooth()



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
