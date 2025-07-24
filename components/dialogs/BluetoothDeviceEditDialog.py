import flet as ft

from helper.PageState import PageState


class BluetoothDeviceEditDialog:
    text = ft.Text("")
    dialog = None
    on_remove = None
    on_disconnect = None

    def __init__(self):
        self.dialog = ft.AlertDialog(
            title=self.text,
            actions=[
                ft.FilledButton("Entfernen", on_click=lambda e, mac_address: self.remove_device(mac_address)),
                ft.FilledButton("Verbindung trennen", on_click=lambda e: self.disconnect_device)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        PageState.page.add(self.dialog)

    def open(self, device_name, on_remove, on_disconnect):
        self.text.value = device_name
        self.text.update()
        self.on_remove = on_remove
        self.on_disconnect = on_disconnect
        self.dialog.open = True
        self.dialog.update()

    def remove_device(self):
        self.on_remove()
        self.close()

    def disconnect_device(self):
        self.on_disconnect()
        self.close()

    def close(self):
        self.dialog.open = False
        self.dialog.update()
