import flet as ft
from helper.Constants import Constants

constants = Constants()

class StationAddDialog:
    dialog = None
    text = ft.Text(f'{constants.current_station_to_add["name"]}')
    on_submit = None
    on_play = None

    def __init__(self, on_play, on_submit):
        self.on_play = on_play
        self.on_submit = on_submit

        self.dialog = ft.AlertDialog(
            content=ft.Column(
                width=500,
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            title=self.text,
            actions=[
                ft.FilledButton("Abspielen", on_click=lambda e: self.play()),
                ft.FilledButton("Zu Liste hinzufügen", on_click=lambda e: self.add_to_list())
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def play(self):
        self.on_play()
        self.close()

    def add_to_list(self):
        self.on_submit()
        self.close()


    def close(self):
        self.dialog.open = False
        self.dialog.update()


    def open(self, element):
        constants.current_station_to_add = element
        self.text.value = element["name"]
        self.dialog.open = True
        self.dialog.update()

    def get(self): return self.dialog
