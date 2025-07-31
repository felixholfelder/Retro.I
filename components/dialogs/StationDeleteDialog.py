import flet as ft

class StationDeleteDialog(ft.AlertDialog):
    submit_callback = None

    def __init__(self):
        super().__init__()

        self.title = ft.Text(f'Sender löschen?'),
        self.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        self.actions = [
            ft.TextButton("Abbrechen", on_click=lambda e: self.close()),
            ft.FilledButton("Löschen", on_click=lambda e: self.submit())
        ]

    def submit(self):
        self.submit_callback()
        self.close()

    def open_dialog(self, submit_callback):
        self.open = True # TODO - test with "self.open(True)" or remove function
        self.submit_callback = submit_callback
        self.update()

    def close(self):
        self.open = False # TODO - test with "self.open(False)" or remove function
        self.update()
