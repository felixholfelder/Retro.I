import flet as ft


class DuplicateDialog(ft.AlertDialog):
    text = ft.Text("")

    def __init__(self):
        super().__init__()

        self.title = self.text
        self.actions = [
            ft.FilledButton("Ok", on_click=lambda e: self.close_dialog())
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def open_dialog(self, name):
        self.text.value = name
        self.text.update()
        self.open = True
        self.update()

    def close_dialog(self):
        self.open = False
        self.update()
