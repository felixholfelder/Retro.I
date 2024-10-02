import flet as ft

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from components.SongInfoRow import SongInfoRow
from components.RadioGrid import RadioGrid
from helper.Audio import Audio
from helper.WifiHelper import WifiHelper
from helper.BluetoothHelper import BluetoothHelper

audio_helper = Audio()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()

class Taskbar:
    taskbar = None
    song_info_row: SongInfoRow = None
    
    wifi_connection_dialog: WifiConnectionDialog = None
    wifi_dialog: WifiDialog = None

    ico_wifi = ft.IconButton(
        icon=ft.icons.WIFI if wifi_helper.is_connected() else ft.icons.WIFI_OFF_ROUNDED,
        icon_size=24,
        icon_color=ft.colors.GREEN if wifi_helper.is_connected() else ft.colors.BLACK
    )

    ico_bluetooth = ft.Icon(name=ft.icons.BLUETOOTH, size=24)

    volume_icon = ft.Icon(
        name=ft.icons.VOLUME_UP_ROUNDED if not audio_helper.is_mute() else ft.icons.VOLUME_OFF_ROUNDED,
        size=24,
        color=ft.colors.BLACK if not audio_helper.is_mute() else ft.colors.RED
    )
    volume_text = ft.Text(f"{audio_helper.get_volume()}%" if not audio_helper.is_mute() else "", size=18)

    def __init__(self, radio_grid: RadioGrid):
        self.song_info_row = SongInfoRow(radio_grid)
        self.taskbar = ft.AppBar(
            toolbar_height=90,
            title=ft.Column([
                ft.Row([
                        ft.Row([
                            self.volume_icon,
                            self.volume_text
                        ]),
                        ft.Text("Retro.I"),
                        ft.Row([
                            self.ico_wifi,
                            self.ico_bluetooth
                        ])
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row([
                    self.song_info_row.get()
                ])
            ])
        )

        self.wifi_connection_dialog = WifiConnectionDialog(self.update)
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
            self.ico_bluetooth.color = ft.colors.BLACK

        if bluetooth_helper.is_connected():
            self.ico_bluetooth.name = ft.icons.BLUETOOTH_CONNECTED_ROUNDED
            self.ico_bluetooth.color = ft.colors.GREEN

        self.ico_bluetooth.update()


    def get(self): return self.taskbar
    def get_song_info(self): return self.song_info_row
    def get_wifi_dialog(self): return self.wifi_dialog
    def get_wifi_connection_dialog(self): return self.wifi_connection_dialog
