import time

from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from components.view.Taskbar import Taskbar
from helper.Audio import Audio
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.SystemHelper import SystemHelper

bluetooth_helper = BluetoothHelper()
system_helper = SystemHelper()
audio_helper = Audio()


class Tabs:
    taskbar: Taskbar = None
    radio_tab: RadioTab = None
    bluetooth_tab: BluetoothTab = None
    settings_tab: SettingsTab = None

    def __init__(
        self,
        taskbar: Taskbar,
        radio_tab: RadioTab,
        bluetooth_tab: BluetoothTab,
        soundboard_tab: SoundboardTab,
        settings_tab: SettingsTab,
    ):
        self.taskbar = taskbar
        self.radio_tab = radio_tab
        self.bluetooth_tab = bluetooth_tab
        self.soundboard_tab = soundboard_tab
        self.settings_tab = settings_tab

    def change_tab(self, e):
        new_tab_index = e.control.selected_index
        self.radio_tab.get_song_info().reset()

        try:
            self.radio_tab.hide()
            self.bluetooth_tab.hide()
            self.settings_tab.hide()
            self.soundboard_tab.hide()
        except Exception:
            pass

        if new_tab_index == 0:
            self.switch_radio_tab()

        if new_tab_index == 1:
            self.switch_bluetooth_tab()

        if new_tab_index == 2:
            if system_helper.is_party_mode():
                self.switch_soundboard_tab()
            else:
                self.switch_settings_tab()

        if new_tab_index == 3:
            self.settings_tab.show()

    def switch_radio_tab(self):
        if bluetooth_helper.is_discovery_on():
            self.bluetooth_tab.get_btn_toggle().toggle_bluetooth_discovery()

        bluetooth_helper.disconnect()
        time.sleep(0.2)
        bluetooth_helper.turn_off()

        self.radio_tab.show()
        self.radio_tab.update()
        self.taskbar.update()

    def switch_bluetooth_tab(self):
        Constants.current_radio_station = {}

        audio_helper.pause()
        bluetooth_helper.turn_on()

        self.taskbar.update()

        self.bluetooth_tab.show()

        self.radio_tab.get_grid().disable_indicator()
        self.radio_tab.get_song_info().reset()

    def switch_soundboard_tab(self):
        self.soundboard_tab.show()

    def switch_settings_tab(self):
        self.settings_tab.show()
