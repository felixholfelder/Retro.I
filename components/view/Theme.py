import flet as ft

from components.NavigationBar import NavigationBar
from components.view.Tabs import Tabs
from components.view.Taskbar import Taskbar
from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from helper.Strip import Strip
from helper.System import System

system_helper = System()


class Theme:
    theme = None
    strip: Strip = None
    taskbar: Taskbar = None

    radio_tab = RadioTab(strip, theme)
    bluetooth_tab = BluetoothTab()
    soundboard_tab = SoundboardTab()
    settings_tab = SettingsTab()

    tabs = Tabs(taskbar, radio_tab, bluetooth_tab, soundboard_tab, settings_tab)

    navbar = NavigationBar(tabs)

    def __init__(self, taskbar: Taskbar, strip: Strip):
        self.strip = strip
        self.taskbar = taskbar

        self.theme = ft.Theme(
            color_scheme_seed='green',
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                },
                thumb_visibility=True,
                thumb_color={
                    ft.MaterialState.HOVERED: ft.colors.GREY_500,
                    ft.MaterialState.DEFAULT: ft.colors.GREY_400,
                },
                thickness=40,
                radius=20,
            )
        )

    def update(self, color):
        self.theme.color_scheme_seed = color
        self.theme.update()

        self.navbar.update(color)

    def get_tabs(self):
        tabs = [self.radio_tab.get(), self.bluetooth_tab.get()]

        if system_helper.is_party_mode():
            tabs.append(self.soundboard_tab.get())

        tabs.append(self.settings_tab.get())

        return tabs

    def get(self): return self.theme
    def get_radio_tab(self): return self.radio_tab
    def get_bluetooth_tab(self): return self.bluetooth_tab
    def get_soundboard_tab(self): return self.soundboard_tab
    def get_settings_tab(self): return self.settings_tab
    def get_navbar(self): return self.navbar