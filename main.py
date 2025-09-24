import threading
import time

import flet as ft

from components.GpioButton import GpioButton
from components.RotaryBass import RotaryBass
from components.RotaryPitch import RotaryPitch
from components.RotaryVolume import RotaryVolume
from components.view.Taskbar import Taskbar
from components.view.Theme import Theme
from helper.Audio import Audio
from helper.AudioEffects import AudioEffects
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.PageState import PageState
from helper.RadioHelper import RadioHelper
from helper.Sounds import Sounds
from helper.Stations import Stations
from helper.Strip import Strip
from helper.SystemHelper import SystemHelper
from helper.WifiHelper import WifiHelper

wifi_helper = WifiHelper()
radio_helper = RadioHelper()
bluetooth_helper = BluetoothHelper()
system_helper = SystemHelper()
stations_helper = Stations()
constants = Constants()
sounds = Sounds()
audio_helper = Audio()
page_helper = PageState()
audio_effects = AudioEffects()


def main(page: ft.Page):
    start = time.time()
    PageState.page = page

    bluetooth_helper.on_startup()

    strip = Strip()
    taskbar = Taskbar()
    theme = Theme(taskbar, strip.run_color)

    page.navigation_bar = theme.navbar
    page.appbar = taskbar
    page.window.maximized = True
    page.window.frameless = True
    page.spacing = 0
    page.theme = theme.get()
    page.title = "Retro.I"

    button = GpioButton(21, audio_helper.play_toast)
    button.activate()

    for item in theme.get_tabs():
        page.add(item)

    theme.radio_tab.radio_grid.reload()
    page.update()

    RotaryVolume(
        on_taskbar_update=taskbar.update,
        on_strip_toggle_mute=strip.toggle_mute,
        on_strip_update_sound=strip.update_sound_strip,
    )
    RotaryBass(on_taskbar_update=taskbar.update)
    RotaryPitch(on_taskbar_update=taskbar.update)

    audio_effects.start()
    audio_helper.startup_sound()

    end = time.time()
    print(f"Startup took: {end-start}")

    def background_processes():
        while True:
            taskbar.update()
            time.sleep(5)

    process = threading.Thread(target=background_processes)
    process.start()


ft.app(main)
