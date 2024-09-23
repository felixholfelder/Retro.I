import flet as ft

from components.view.Taskbar import Taskbar
from helper.BluetoothHelper import BluetoothHelper

bluetooth_helper = BluetoothHelper()

class BluetoothDeviceConnected:
    btn = None
    taskbar = None

    ico_device_connected = ft.Icon(ft.icons.PHONELINK_OFF)
    txt_device_connected = ft.Text("Kein Gerät verbunden", style=ft.TextStyle(size=20))

    def __init__(self, taskbar: Taskbar, on_connected):
        self.taskbar = taskbar

        self.btn = ft.TextButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.ico_device_connected,
                    self.txt_device_connected
                ],
            ),
            width=500,
            height=80,
            on_click=lambda e: self.update_connected_device(on_connected),
        )

    def reset_connected_device(self):
        self.txt_device_connected.value = "Kein Gerät verbunden"
        self.ico_device_connected.name = ft.icons.PHONELINK_OFF

    def update_connected_device(self, on_connected):
        name = bluetooth_helper.get_device_name()
        if name != "":
            self.txt_device_connected.value = f"Verbunden mit: {name}"
            self.ico_device_connected.name = ft.icons.PHONELINK
            on_connected()
        else:
            self.reset_connected_device()

        self.ico_device_connected.update()
        self.txt_device_connected.update()
        self.taskbar.update()

    def get(self): return self.btn