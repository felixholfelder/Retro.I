import flet as ft

from components.view.Tabs import Tabs
from helper.ColorHelper import ColorHelper
from helper.SystemHelper import System

system_helper = System()
color_helper = ColorHelper()

ICON_SIZE = 28

class NavigationBar:
    bar = None
    icon_color = ft.colors.BLACK

    def __init__(self, tabs: Tabs):
        destinations = []
        destinations.append(
            ft.NavigationDestination(
                label="Radiosender",
                icon_content=ft.Icon(ft.icons.RADIO_OUTLINED, size=ICON_SIZE, color=self.icon_color),
                selected_icon_content=ft.Icon(ft.icons.RADIO, size=ICON_SIZE)
            )
        )

        destinations.append(
            ft.NavigationDestination(
                label="Bluetooth",
                icon_content=ft.Icon(ft.icons.BLUETOOTH_OUTLINED, size=ICON_SIZE, color=self.icon_color),
                selected_icon_content=ft.Icon(ft.icons.BLUETOOTH, size=ICON_SIZE)
            )
        )

        if system_helper.is_party_mode():
            destinations.append(
                ft.NavigationDestination(
                    label="Soundboard",
                    icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD_OUTLINED, size=ICON_SIZE, color=self.icon_color),
                    selected_icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD, size=ICON_SIZE)
                ),
            )

        destinations.append(
            ft.NavigationDestination(
                label="Einstellungen",
                icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED, size=ICON_SIZE, color=self.icon_color),
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
        self.icon_color = color_helper.get_navbar_icon_color(color)
        self.bar.update()
        for i in self.bar.destinations:
            i.update()
    
    def get_bgcolor(self):
        return self.bar.bgcolor

    def get(self): return self.bar
