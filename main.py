import threading
import time
import vlc

import flet as ft

from components.GpioButton import GpioButton
from components.RotaryBass import RotaryBass
from components.RotaryVolume import RotaryVolume
from components.RotaryPitch import RotaryPitch
from components.view.Taskbar import Taskbar
from components.view.Theme import Theme
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.RadioHelper import RadioHelper
from helper.Sounds import Sounds
from helper.Stations import Stations
from helper.Strip import Strip
from helper.SystemHelper import System
from helper.WifiHelper import WifiHelper
from helper.Audio import Audio
from helper.PageHelper import PageHelper

wifi_helper = WifiHelper()
radio_helper = RadioHelper()
bluetooth_helper = BluetoothHelper()
system_helper = System()
stations_helper = Stations()
constants = Constants()
sounds = Sounds()
audio_helper = Audio()
page_helper = PageHelper()
audio_effects = AudioEffects()

def main(page: ft.Page):
    strip = Strip()
    taskbar = Taskbar()
    theme = Theme(taskbar, strip, page)

    page.navigation_bar = theme.get_navbar().get()
    page.appbar = taskbar.get()
    page.window.maximized = True
    page.window.frameless = True
    page.spacing = 0
    page.theme = theme.get()
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.title = "Retro.I"

    button = GpioButton(21, audio_helper.play_toast)
    button.activate()

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

    PageHelper.page = page

    RotaryVolume(taskbar, strip)
    RotaryBass(taskbar)
    RotaryPitch(taskbar)

    audio_helper.startup_sound()
    
    def background_processes():
        audio_effects.start()
        while True:
            taskbar.update()
            theme.get_radio_tab().update()
            time.sleep(5)

    process = threading.Thread(target=background_processes)
    process.start()


ft.app(main)
