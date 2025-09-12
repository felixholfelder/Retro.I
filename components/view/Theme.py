import flet as ft

from components.NavigationBar import NavigationBar
from components.view.Tabs import Tabs
from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from components.view.Taskbar import Taskbar
from helper.PageState import PageState
from helper.Strip import Strip
from helper.SystemHelper import SystemHelper
from scripts import button  # noqa: F401

system_helper = SystemHelper()


class Theme:
    theme = None
    strip: Strip = None
    taskbar: Taskbar = None

    radio_tab = None
    bluetooth_tab = None
    soundboard_tab = None
    settings_tab = None

    tabs = None
    navbar = None
    page: ft.Page = None

    def __init__(self, taskbar: Taskbar, on_strip_run_color):
        self.page = PageState.page
        self.taskbar = taskbar

        self.theme = ft.Theme(
            color_scheme_seed="green",
            scrollbar_theme=ft.ScrollbarTheme(
                thumb_visibility=False,
                track_visibility=False,
            ),
        )

        self.radio_tab = RadioTab(on_strip_run_color, self.on_updated_radio_station, self.update)
        self.bluetooth_tab = BluetoothTab(self.taskbar)
        self.soundboard_tab = SoundboardTab()
        self.settings_tab = SettingsTab()
        self.tabs = Tabs(
            taskbar,
            self.radio_tab,
            self.bluetooth_tab,
            self.soundboard_tab,
            self.settings_tab,
        )
        self.navbar = NavigationBar(self.tabs)

    def update(self):
        self.page.update()

    def on_updated_radio_station(self, color):
        self.theme.color_scheme_seed = color
        self.navbar.update_color(color)
        self.radio_tab.update()
        self.page.update()

    def get_tabs(self):
        tabs = []
        tabs.append(self.radio_tab)
        tabs.append(self.bluetooth_tab)

        if system_helper.is_party_mode():
            tabs.append(self.soundboard_tab)

        tabs.append(self.settings_tab)

        return tabs

    def get(self):
        return self.theme

    def get_radio_tab(self):
        return self.radio_tab
