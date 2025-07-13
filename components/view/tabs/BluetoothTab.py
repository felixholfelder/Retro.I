import flet as ft
import threading
import time

from components.BluetoothDeviceConnected import BluetoothDeviceConnected
from components.BluetoothDiscoveryToggle import BluetoothDiscoveryToggle
from components.view.Taskbar import Taskbar


class BluetoothTab:
    tab = None
    taskbar: Taskbar = None
    btn_toggle_discovery = None
    device_connected = None
    update_device_connection = False

    def __init__(self, taskbar: Taskbar):
        self.taskbar = taskbar
        self.btn_toggle_discovery = BluetoothDiscoveryToggle()
        self.device_connected = BluetoothDeviceConnected(taskbar, self.btn_toggle_discovery.disable_discovery)

        self.tab = ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                spacing=50,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.btn_toggle_discovery.get(),
                    self.device_connected.get()
                ]
            ),
            visible=False,
        )

    def update(self):
        self.tab.update()

    def show(self):
        self.tab.visible = True
        self.update_device_connection = True
        self.process_bluetooth_connection()
        self.update()

    def hide(self):
        self.tab.visible = False
        self.update_device_connection = False
        self.update()
        
    def update_connected_device(self):
        while self.update_device_connection:
            connected = self.device_connected.update_connected_device(self.get_btn_toggle().disable_discovery)
            if connected:
                self.update_device_connection = False
                
            time.sleep(0.5)

    def process_bluetooth_connection(self):
        process = threading.Thread(target=self.update_connected_device)
        process.start()

    def get(self): return self.tab
    def get_btn_toggle(self): return self.btn_toggle_discovery
    def get_device_connected(self): return self.device_connected
