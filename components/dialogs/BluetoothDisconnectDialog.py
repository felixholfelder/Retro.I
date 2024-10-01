import flet as ft


class BluetoothDisconnectDialog:
    dialog = None
    title = ft.Text("")

    def __init__(self):
        self.dialog = ft.AlertDialog(
            title=self.title,
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def submit(self, submit_callback):
        submit_callback()
        self.close()

    def open(self, name):
        self.title.value = f'Verbindung zu "{name}" wird getrennt...'
        self.title.update()

        self.dialog.open = True
        self.dialog.update()

    def close(self):
        self.dialog.open = False
        self.dialog.update()

    def get(self): return self.dialog


