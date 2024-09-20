import flet as ft
from helper.BluetoothHelper import BluetoothHelper

bluetooth_helper = BluetoothHelper()

class BluetoothDiscoveryToggle:
    btn = None
    ico_discovery_status = ft.Icon(ft.icons.BLUETOOTH_DISABLED)
    txt_discovery_status = ft.Text("Bluetooth nicht sichtbar", style=ft.TextStyle(size=20))

    def __init__(self):
        self.btn = ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.ico_discovery_status,
                    self.txt_discovery_status
                ],
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED,
            ),
            width=500,
            height=80,
            on_click=lambda e: self.toggle_bluetooth_discovery(),
        )

    def enable_discovery(self):
        bluetooth_helper.bluetooth_discovery_on()
        self.txt_discovery_status.value = "Bluetooth sichtbar"
        self.ico_discovery_status.name = ft.icons.BLUETOOTH
        self.btn.style.bgcolor = ft.colors.GREEN

        self.txt_discovery_status.update()
        self.ico_discovery_status.update()
        self.btn.update()


    def disable_discovery(self):
        bluetooth_helper.bluetooth_discovery_off()
        self.txt_discovery_status.value = "Bluetooth nicht sichtbar"
        self.ico_discovery_status.name = ft.icons.BLUETOOTH_DISABLED
        self.btn.style.bgcolor = ft.colors.RED

        self.txt_discovery_status.update()
        self.ico_discovery_status.update()
        self.btn.update()


    def toggle_bluetooth_discovery(self):
        discovery_on = bluetooth_helper.is_discovery_on()
        if discovery_on:
            self.disable_discovery()
        else:
            self.enable_discovery()

    def get(self): return self.btn