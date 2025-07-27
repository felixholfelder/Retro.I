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
    bluetooth_device_edit_dialog = None

    def __init__(self, taskbar: Taskbar):
        self.taskbar = taskbar
        self.btn_toggle_discovery = BluetoothDiscoveryToggle(self.start_bluetooth_update_process, self.stop_bluetooth_update_process)
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
                    ft.Text("Gekoppelte Geräte:", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT, expand=True),
                    self.device_connected.get(),
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

    def get(self): return self.tab
    def get_btn_toggle(self): return self.btn_toggle_discovery
    def get_device_connected(self): return self.device_connected
