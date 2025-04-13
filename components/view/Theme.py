import flet as ft

from scripts import button

from components.NavigationBar import NavigationBar
from components.view.Tabs import Tabs
from components.view.Taskbar import Taskbar
from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from helper.Strip import Strip
from helper.SystemHelper import System

system_helper = System()


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
    page = None

    def __init__(self, taskbar: Taskbar, strip: Strip, page: ft.Page):
        self.strip = strip
        self.taskbar = taskbar
        self.page = page

        self.theme = ft.Theme(
            color_scheme_seed='green',
            scrollbar_theme=ft.ScrollbarTheme(
                thumb_visibility=False,
                track_visibility=False,
            )
        )

        
        self.radio_tab = RadioTab(strip, self)
        self.bluetooth_tab = BluetoothTab(self.taskbar)
        self.soundboard_tab = SoundboardTab()
        self.settings_tab = SettingsTab()
        self.tabs = Tabs(taskbar, self.radio_tab, self.bluetooth_tab, self.soundboard_tab, self.settings_tab)
        self.navbar = NavigationBar(self.tabs)

    def update(self, color):
        self.theme.color_scheme_seed = color
        self.navbar.update(color)
        self.page.update()
        self.radio_tab.update()
        self.page.update()

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
    
    def get_search_dialog(self): return self.get_radio_tab().get_song_info().get_search_dialog()
    def get_station_add_dialog(self): return self.get_radio_tab().get_song_info().get_station_add_dialog()
