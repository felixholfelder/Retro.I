import flet as ft

from components.dialogs.WifiConnectionDialog import WifiConnectionDialog
from components.dialogs.WifiDialog import WifiDialog
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.WifiHelper import WifiHelper
from helper.BluetoothHelper import BluetoothHelper

audio_helper = Audio()
audio_effects = AudioEffects()
wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()

class Taskbar(ft.AppBar):
    wifi_connection_dialog: WifiConnectionDialog = None
    wifi_dialog: WifiDialog = None

    ico_wifi = ft.IconButton(icon=ft.icons.WIFI, icon_size=25, icon_color=ft.colors.GREEN)
    ico_bluetooth = ft.Icon(name=ft.icons.BLUETOOTH, size=25)
    
    ico_volume = ft.Icon(name=ft.icons.VOLUME_UP_ROUNDED, size=25)
    txt_volume = ft.Text(f"{audio_helper.get_volume()}%", size=18)
    
    ico_bass = ft.Icon(name=ft.icons.SURROUND_SOUND, size=25)
    txt_bass = ft.Text(f"+{audio_effects.get_bass_value()} dB", size=18)
    
    ico_pitch = ft.Icon(name=ft.icons.HEIGHT, size=25)
    txt_pitch = ft.Text(audio_effects.get_pitch_value(), size=18)

    def __init__(self):
        super().__init__()

        self.leading=ft.Row([
                ft.Row([self.ico_volume, self.txt_volume]),
                ft.VerticalDivider(),
                ft.Row([self.ico_bass, self.txt_bass]),
                ft.VerticalDivider(),
                ft.Row([self.ico_pitch, self.txt_pitch]),
                ft.VerticalDivider(),
            ])
        self.title=ft.Text("Retro.I")
        self.center_title=True
        self.bgcolor=ft.colors.SURFACE_VARIANT
        self.toolbar_height=40
        self.actions=[self.ico_wifi, self.ico_bluetooth]

        self.wifi_connection_dialog = WifiConnectionDialog(self.update)
        self.wifi_dialog = WifiDialog(self.wifi_connection_dialog)
        self.ico_wifi.on_click = lambda e: self.wifi_dialog.open_dialog()

    def update(self):
        self.update_volume_icon()
        self.update_bass()
        self.update_pitch()
        self.update_wifi()
        self.update_bluetooth_icon()
        super().update()

    def update_wifi(self):
        self.ico_wifi.name = ft.icons.WIFI if wifi_helper.is_connected() else ft.icons.WIFI_OFF_ROUNDED
        self.ico_wifi.color = ft.colors.GREEN if wifi_helper.is_connected() else ft.colors.BLACK
        self.ico_wifi.update()

    def update_bluetooth_icon(self):
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

    def update_volume_icon(self):
        self.ico_volume.name = ft.icons.VOLUME_OFF_ROUNDED if audio_helper.is_mute() else ft.icons.VOLUME_UP_ROUNDED
        self.ico_volume.color = ft.colors.RED if audio_helper.is_mute() else ft.colors.BLACK
        self.ico_volume.update()
        self.txt_volume.value = f"{audio_helper.get_volume()}%" if not audio_helper.is_mute() else ""
        self.txt_volume.update()

    def update_bass(self):
        self.txt_bass.value = f"+{audio_effects.get_bass_value()} dB" if audio_effects.get_bass_value() > 0 else f"{audio_effects.get_bass_value()} dB"
        self.txt_bass.update()

    def update_pitch(self):
        self.txt_pitch.value = audio_effects.get_pitch_value()
        self.txt_pitch.update()
