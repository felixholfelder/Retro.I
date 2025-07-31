import flet as ft

from helper.BluetoothHelper import BluetoothHelper

bluetooth_helper = BluetoothHelper()


class BluetoothDiscoveryToggle(ft.FilledButton):
    ico_discovery_status = ft.Icon(ft.icons.BLUETOOTH_DISABLED)
    txt_discovery_status = ft.Text("Bluetooth nicht sichtbar", style=ft.TextStyle(size=20))

    on_discovery_enabled = None
    on_discovery_disabled = None

    def __init__(self, on_dicovery_enabled, on_dicovery_disabled):
        super().__init__()
        self.on_discovery_enabled = on_dicovery_enabled
        self.on_discovery_disabled = on_dicovery_disabled

        # Button attributes
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.ico_discovery_status,
                self.txt_discovery_status
            ]
        )
        self.style = ft.ButtonStyle(bgcolor=ft.colors.RED)
        self.width = 500
        self.height = 80
        self.on_click = lambda e: self.toggle_bluetooth_discovery()

    def enable_discovery(self):
        bluetooth_helper.bluetooth_discovery_on()
        self.txt_discovery_status.value = "Bluetooth sichtbar"
        self.ico_discovery_status.name = ft.icons.BLUETOOTH
        self.style.bgcolor = ft.colors.GREEN

        self.txt_discovery_status.update()
        self.ico_discovery_status.update()
        self.update()

        self.on_discovery_enabled()

    def disable_discovery(self):
        bluetooth_helper.bluetooth_discovery_off()
        self.txt_discovery_status.value = "Bluetooth nicht sichtbar"
        self.ico_discovery_status.name = ft.icons.BLUETOOTH_DISABLED
        self.style.bgcolor = ft.colors.RED

        self.txt_discovery_status.update()
        self.ico_discovery_status.update()
        self.update()

        self.on_discovery_disabled()

    def toggle_bluetooth_discovery(self):
        discovery_on = bluetooth_helper.is_discovery_on()
        if discovery_on:
            self.disable_discovery()
        else:
            self.enable_discovery()
