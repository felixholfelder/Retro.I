import flet as ft


class DuplicateDialog:
    text = ft.Text("")
    dialog = None

    def __init__(self):
        self.dialog = ft.AlertDialog(
            title=self.text,
            actions=[
                ft.FilledButton("Ok", on_click=lambda e: self.close())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def open(self, name):
        self.text.value = name
        self.text.update()
        self.dialog.open = True
        self.dialog.update()

    def close(self):
        self.dialog.open = False
        self.dialog.update()

    def get(self): return self.dialog
