import flet as ft


class StationDeleteDialog:
    dialog = None
    page = None

    def __init__(self, submit_callback, page):
        self.page = page
        self.dialog = ft.AlertDialog(
            title=ft.Text(f'Sender löschen?'),
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            actions=[
                ft.TextButton("Abbrechen", on_click=lambda e: self.close()),
                ft.FilledButton("Löschen", on_click=lambda e: self.submit(submit_callback))
            ]
        )

    def submit(self, submit_callback):
        submit_callback()
        self.close()

    def get(self): return self.dialog

    def open(self):
        self.dialog.open = True
        self.page.update()

    def close(self):
        self.dialog.open = False
        self.page.update()
