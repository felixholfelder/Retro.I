import flet as ft

from components.view.Tabs import Tabs
from helper.ColorHelper import ColorHelper
from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()
color_helper = ColorHelper()

ICON_SIZE = 28


class NavigationBar(ft.NavigationBar):
    icon_color = ft.colors.BLACK

    def __init__(self, tabs: Tabs):
        super().__init__()

        self.bgcolor = "green"
        self.on_change = tabs.change_tab
        self.selected_index = 0
        self.destinations = self.get_destinations()

    def update_color(self, color):
        self.bgcolor = color
        self.icon_color = color_helper.get_navbar_icon_color(color)
        self.update()
        for i in self.destinations:
            i.update()

    def get_destinations(self):
        destinations = [
            ft.NavigationDestination(
                label="Radiosender",
                icon_content=ft.Icon(ft.icons.RADIO_OUTLINED, size=ICON_SIZE, color=self.icon_color),
                selected_icon_content=ft.Icon(ft.icons.RADIO, size=ICON_SIZE),
            ),
            ft.NavigationDestination(
                label="Bluetooth",
                icon_content=ft.Icon(ft.icons.BLUETOOTH_OUTLINED, size=ICON_SIZE, color=self.icon_color),
                selected_icon_content=ft.Icon(ft.icons.BLUETOOTH, size=ICON_SIZE),
            ),
        ]

        if system_helper.is_party_mode():
            destinations.append(
                ft.NavigationDestination(
                    label="Soundboard",
                    icon_content=ft.Icon(
                        ft.icons.SPACE_DASHBOARD_OUTLINED,
                        size=ICON_SIZE,
                        color=self.icon_color,
                    ),
                    selected_icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD, size=ICON_SIZE),
                ),
            )

        destinations.append(
            ft.NavigationDestination(
                label="Einstellungen",
                icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED, size=ICON_SIZE, color=self.icon_color),
                selected_icon_content=ft.Icon(ft.icons.SETTINGS, size=ICON_SIZE),
            )
        )

        return destinations
