import flet as ft


class BluetoothDeviceEditDialog(ft.AlertDialog):
    text = ft.Text("")
    on_remove = None

    def __init__(self):
        super().__init__()

        self.title = self.text
        self.actions = [ft.FilledButton("Entfernen", on_click=lambda e: self.remove_device())]
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self, device_name, on_remove):
        self.text.value = device_name
        self.text.update()
        self.on_remove = on_remove
        self.open = True
        self.update()

    def remove_device(self):
        self.on_remove()
        self.close()

    def close(self):
        self.open = False
        self.update()
