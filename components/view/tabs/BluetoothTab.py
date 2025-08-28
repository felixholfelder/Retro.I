import flet as ft
import threading
import time

from components.BluetoothDeviceConnected import BluetoothDeviceConnected
from components.BluetoothDiscoveryToggle import BluetoothDiscoveryToggle
from components.view.Taskbar import Taskbar

class BluetoothTab(ft.Column):
    taskbar: Taskbar = None
    btn_toggle_discovery = None
    device_connected = None
    update_device_connection = False
    bluetooth_device_edit_dialog = None

    def __init__(self, taskbar: Taskbar):
        super().__init__()

        self.taskbar = taskbar
        self.btn_toggle_discovery = BluetoothDiscoveryToggle(self.start_bluetooth_update_process, self.stop_bluetooth_update_process)
        self.device_connected = BluetoothDeviceConnected(taskbar, self.btn_toggle_discovery.disable_discovery)

        self.alignment=ft.alignment.center
        self.expand=True
        self.visible=False
        self.controls=[
            ft.Row(
                spacing=50,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.btn_toggle_discovery,
                ]
            ),
            ft.Divider(),
            ft.Text("Gekoppelte Geräte:", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
            self.device_connected.get(),
        ]

    def show(self):
        self.visible = True
        self.update_device_connection = True
        self.process_bluetooth_connection()
        self.update()

    def hide(self):
        self.visible = False
        self.update_device_connection = False
        self.update()

    def update_connected_device(self):
        while self.update_device_connection:
            connected = self.device_connected.update_connected_device()
            if connected:
                self.update_device_connection = False
            self.device_connected.reload_devices()
            time.sleep(1)

    def start_bluetooth_update_process(self):
        self.update_device_connection = True
        self.process_bluetooth_connection()

    def stop_bluetooth_update_process(self):
        self.update_device_connection = False

    def process_bluetooth_connection(self):
        process = threading.Thread(target=self.update_connected_device)
        process.start()

    def get_btn_toggle(self): return self.btn_toggle_discovery
    def get_device_connected(self): return self.device_connected
