import flet as ft

from components.RadioGrid import RadioGrid
from components.dialogs.RadioSearchDialog import RadioSearchDialog
from helper.Constants import Constants
from helper.PageState import PageState
from helper.RadioHelper import RadioHelper

constants = Constants()
radio_helper = RadioHelper()


class SongInfoRow(ft.Container):
    song_info_station = ft.Text("Kein Radiosender ausgewählt", weight=ft.FontWeight.BOLD, size=16)
    song_info_title = ft.Text("", size=16, overflow=ft.TextOverflow.ELLIPSIS, expand=True)

    radio_search_dialog: RadioSearchDialog = None

    def __init__(self, radio_grid: RadioGrid):
        super().__init__()

        self.radio_search_dialog = RadioSearchDialog(radio_grid)
        self.content = ft.Row([
            ft.Icon(ft.icons.MUSIC_NOTE, size=28),
            self.song_info_station,
            self.song_info_title,
            ft.TextButton(
                "Sendersuche",
                icon=ft.icons.SEARCH,
                on_click=lambda e: self.radio_search_dialog.open_dialog(),
                # style=ft.ButtonStyle(
                #    text_style=ft.TextStyle(size=16)
                # )
            )
        ])
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, "gray"))
        self.padding = ft.padding.only(bottom=10)

        PageState.page.add(self.radio_search_dialog)

    def reload(self):
        try:
            title = radio_helper.get_song_info(Constants.current_radio_station["src"])

            if title != "":
                self.song_info_station.value = Constants.current_radio_station["name"]
                self.song_info_title.value = title
            else:
                self.song_info_station.value = Constants.current_radio_station["name"]
                self.song_info_title.value = ""
        except:
            pass

        self.update()

    def update(self):
        self.song_info_station.update()
        self.song_info_title.update()
        super().update()

    def reset(self):
        self.song_info_station.value = "Kein Radiosender ausgewählt"
        self.song_info_title.value = ""
        self.update()
