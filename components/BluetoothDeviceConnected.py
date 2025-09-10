import flet as ft

import time

from components.dialogs.BluetoothDeviceEditDialog import BluetoothDeviceEditDialog
from components.view.Taskbar import Taskbar
from helper.BluetoothHelper import BluetoothHelper
from helper.Audio import Audio
from helper.PageState import PageState

bluetooth_helper = BluetoothHelper()
audio_helper = Audio()

class BluetoothDeviceConnected:
    listview = ft.ListView(spacing=10, expand=True)
    taskbar = None
    paired_devices = []
    bluetooth_device_edit_dialog: BluetoothDeviceEditDialog = None
    on_connected = None
    on_disconnected = None

    def __init__(self, taskbar: Taskbar, on_connected, on_disconnected):
        self.taskbar = taskbar
        self.bluetooth_device_edit_dialog = BluetoothDeviceEditDialog()
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected

        PageState.page.add(self.bluetooth_device_edit_dialog)

    def update_connected_device(self):
        name = bluetooth_helper.get_connected_device_name()
        if name != "":
            audio_helper.bluetooth_connected()
            self.on_connected()
            while not any(obj["name"] == name for obj in self.paired_devices):
                self.reload_devices()
                time.sleep(1)

        self.taskbar.update()
        
        return name != ""

    def reload_devices(self):
        devices = bluetooth_helper.get_paired_devices()
        self.paired_devices = devices
        self.listview.controls = []
        for device in devices:
            ico = ft.Icon(ft.icons.DONE, visible=False)
            btn = ft.TextButton(
                content=ft.Container(
                    content=ft.Row([
                        ico,
                        ft.Column(
                            controls=[
                                ft.Text(device["name"], size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(device["mac_address"], size=14)
                            ]
                        ),
                    ]),
                    on_click=lambda e, name=device: self.on_device_click(name),
                    on_long_press=lambda e, name=device: self.on_device_long_click(name)
                )
            )

            if bluetooth_helper.get_connected_device_mac().upper() == device["mac_address"].upper():
                ico.visible = True

            self.listview.controls.append(btn)
        self.listview.update()

    def on_device_click(self, device):
        if bluetooth_helper.get_connected_device_mac().upper() == device["mac_address"].upper():
            bluetooth_helper.disconnect(device["mac_address"])
            audio_helper.bluetooth_disconnected()
            self.on_disconnected()
        
        self.reload_devices()

    def on_device_long_click(self, device):
        def on_device_remove():
            bluetooth_helper.remove_device(device["mac_address"])
            self.reload_devices()

        self.bluetooth_device_edit_dialog.open_dialog(device["name"], on_device_remove)

    def get(self): return self.listview
