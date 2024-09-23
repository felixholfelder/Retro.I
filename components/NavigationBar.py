import flet as ft

from components.view.Tabs import Tabs
from helper.System import System

system_helper = System()

ICON_SIZE = 28

class NavigationBar:
    bar = None

    def __init__(self, tabs: Tabs):
        destinations = []
        destinations.append(
            ft.NavigationDestination(
                label="Radiosender",
                icon_content=ft.Icon(ft.icons.RADIO_OUTLINED, size=ICON_SIZE),
                selected_icon_content=ft.Icon(ft.icons.RADIO, size=ICON_SIZE)
            )
        )

        destinations.append(
            ft.NavigationDestination(
                label="Bluetooth",
                icon_content=ft.Icon(ft.icons.BLUETOOTH_OUTLINED, size=ICON_SIZE),
                selected_icon_content=ft.Icon(ft.icons.BLUETOOTH, size=ICON_SIZE)
            )
        )

        if system_helper.is_party_mode():
            destinations.append(
                ft.NavigationDestination(
                    label="Soundboard",
                    icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD_OUTLINED, size=ICON_SIZE),
                    selected_icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD, size=ICON_SIZE)
                ),
            )

        destinations.append(
            ft.NavigationDestination(
                label="Einstellungen",
                icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED, size=ICON_SIZE),
                selected_icon_content=ft.Icon(ft.icons.SETTINGS, size=ICON_SIZE),
            )
        )

        self.bar = ft.NavigationBar(
            bgcolor="green",
            on_change=tabs.change_tab,
            selected_index=0,
            destinations=destinations
        )

    def update(self, color):
        self.bar.bgcolor = color
        self.bar.update()

    def get(self): return self.bar