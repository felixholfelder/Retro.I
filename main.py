import threading
import time

import flet as ft

from scripts import button

from components.GpioButton import GpioButton
from components.Rotary import Rotary
from components.view.Taskbar import Taskbar
from components.view.Theme import Theme
from helper.Audio import Audio
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.RadioHelper import RadioHelper
from helper.Sounds import Sounds
from helper.Stations import Stations
from helper.Strip import Strip
from helper.SystemHelper import System
from helper.WifiHelper import WifiHelper

wifi_helper = WifiHelper()
radio_helper = RadioHelper()
bluetooth_helper = BluetoothHelper()
audio_helper = Audio()
system_helper = System()
system_helper.init_party_mode()
stations_helper = Stations()
constants = Constants()
sounds = Sounds()


def main(page: ft.Page):
    page.add(audio_helper.init())
    page.update()

    strip = Strip()
    taskbar = Taskbar()
    theme = Theme(taskbar, strip, page)

    page.navigation_bar = theme.get_navbar().get()
    page.appbar = taskbar.get()
    #page.window_maximized = True
    #page.window_frameless = True
    page.spacing = 0
    page.theme = theme.get()
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.title = "Retro.I" 

    GpioButton(21, audio_helper.play_toast)
    Rotary(taskbar, strip)

    page.add(taskbar.get_wifi_dialog().get())
    page.add(taskbar.get_wifi_connection_dialog().get())
    page.add(theme.get_radio_tab().get_song_info().get_search_dialog().get())
    page.add(theme.get_radio_tab().get_song_info().get_station_add_dialog().get())
    page.add(theme.get_radio_tab().get_song_info().get_station_add_dialog().get_duplicate_dialog().get())
    page.add(theme.get_radio_tab().get_grid().get_delete_dialog().get())
    page.add(theme.get_settings_tab().get_shutdown_dialog().get())
    page.add(theme.get_settings_tab().get_led_dialog().get())
    page.add(theme.get_settings_tab().get_info_dialog().get())
    page.add(theme.get_settings_tab().get_credits_dialog().get())
    
    page.add(ft.Column(theme.get_tabs()))
    theme.get_radio_tab().get_grid().reload()
    page.update()

    audio_helper.startup_sound()
    
    taskbar.update()
    
    def background_processes():
        while True:
            theme.get_bluetooth_tab().get_device_connected().update_connected_device(theme.get_bluetooth_tab().get_btn_toggle().disable_discovery)
            taskbar.update()
            theme.get_radio_tab().update()
            time.sleep(5)

    process = threading.Thread(target=background_processes())
    process.start()


ft.app(main)
