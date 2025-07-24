import flet as ft
import threading
import time

from components.BluetoothDeviceConnected import BluetoothDeviceConnected, bluetooth_helper
from components.BluetoothDiscoveryToggle import BluetoothDiscoveryToggle
from components.dialogs.BluetoothDeviceEditDialog import BluetoothDeviceEditDialog
from components.view.Taskbar import Taskbar


class BluetoothTab:
    tab = None
    taskbar: Taskbar = None
    btn_toggle_discovery = None
    device_connected = None
    update_device_connection = False

    listview_paired_devices = ft.ListView(spacing=10, expand=True)
    paired_devices = []
    bluetooth_device_edit_dialog: BluetoothDeviceEditDialog = None

    def __init__(self, taskbar: Taskbar):
        self.bluetooth_device_edit_dialog = BluetoothDeviceEditDialog()
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
                    ft.Text("Gekoppelte Geräte:", size=20, weight=ft.FontWeight.BOLD),
                    self.listview_paired_devices
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
            devices = bluetooth_helper.get_paired_devices()
            self.paired_devices = devices
            self.listview_paired_devices.controls = []
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
                    )
                )

                if bluetooth_helper.get_connected_device_mac().upper() == device["mac_address"].upper():
                    ico.visible = True
                    self.update_device_connection = False

                self.listview_paired_devices.controls.append(btn)
            self.listview_paired_devices.update()
                
            time.sleep(0.5)

    def on_device_click(self, device):
        def on_device_remove():
            print(device["mac_address"])
            bluetooth_helper.remove_paired_device(device["mac_address"])
            self.update_device_connection = True
            self.process_bluetooth_connection()

        def on_device_disconnect():
            print(device["mac_address"])
            bluetooth_helper.disconnect(device["mac_address"])
            self.update_device_connection = True
            self.process_bluetooth_connection()

        if bluetooth_helper.get_connected_device_mac().upper() == device["mac_address"].upper():
            self.bluetooth_device_edit_dialog.open(
                device_name=device["name"],
                on_remove=on_device_remove,
                on_disconnect=on_device_disconnect
            )
        else:
            # TODO - disable listview
            self.listview_paired_devices.disabled = True
            bluetooth_helper.connect(device["mac_address"])
            self.listview_paired_devices.disabled = False

    def process_bluetooth_connection(self):
        process = threading.Thread(target=self.update_connected_device)
        process.start()

    def get(self): return self.tab
    def get_btn_toggle(self): return self.btn_toggle_discovery
    def get_device_connected(self): return self.device_connected
