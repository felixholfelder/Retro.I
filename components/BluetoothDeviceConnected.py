import flet as ft

from components.dialogs.BluetoothDeviceEditDialog import BluetoothDeviceEditDialog
from components.view.Taskbar import Taskbar
from helper.BluetoothHelper import BluetoothHelper
from helper.Audio import Audio

bluetooth_helper = BluetoothHelper()
audio_helper = Audio()

class BluetoothDeviceConnected:
    listview = ft.ListView(spacing=10, expand=True)
    taskbar = None
    paired_devices = []
    bluetooth_device_edit_dialog = BluetoothDeviceEditDialog()

    ico_device_connected = ft.Icon(ft.icons.PHONELINK_OFF)
    txt_device_connected = ft.Text("", style=ft.TextStyle(size=20))

    def __init__(self, taskbar: Taskbar, on_connected):
        self.taskbar = taskbar
        self.reset_connected_device()

        self.listview = ft.TextButton(
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
        name = bluetooth_helper.get_connected_device_name()
        if name != "":
            self.txt_device_connected.value = f"Verbunden mit: {name}"
            self.ico_device_connected.name = ft.icons.PHONELINK
            
            audio_helper.bluetooth_connected()
            on_connected()
        else:
            self.reset_connected_device()

        self.ico_device_connected.update()
        self.txt_device_connected.update()
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
        else:
            # TODO - disable listview
            self.listview.disabled = True
            bluetooth_helper.connect(device["mac_address"])
            self.listview.disabled = False
        self.reload_devices()

    def on_device_long_click(self, device):
        def on_device_remove():
            bluetooth_helper.remove_device(device["mac_address"])
            self.reload_devices()

        self.bluetooth_device_edit_dialog.open(device["name"], on_device_remove)

    def get(self): return self.listview
