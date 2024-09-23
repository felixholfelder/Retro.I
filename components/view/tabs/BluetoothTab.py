import flet as ft

from components.BluetoothDeviceConnected import BluetoothDeviceConnected
from components.BluetoothDiscoveryToggle import BluetoothDiscoveryToggle
from components.view.Taskbar import Taskbar


class BluetoothTab:
    tab = None
    taskbar: Taskbar = None
    btn_toggle_discovery = BluetoothDiscoveryToggle()
    device_connected = BluetoothDeviceConnected(taskbar, btn_toggle_discovery.disable_discovery())

    def __init__(self):

        self.tab = ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                spacing=50,
                controls=[
                    self.btn_toggle_discovery.get(),
                    self.device_connected.get()
                ]
            ),
            visible=False,
        )

    def update(self):
        self.tab.update()

    def get(self): return self.tab
    def get_btn_toggle(self): return self.btn_toggle_discovery
    def get_device_connected(self): return self.device_connected