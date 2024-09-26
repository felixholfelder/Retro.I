from components.view.Taskbar import Taskbar
from components.view.tabs.BluetoothTab import BluetoothTab
from components.view.tabs.RadioTab import RadioTab
from components.view.tabs.SettingsTab import SettingsTab
from components.view.tabs.SoundboardTab import SoundboardTab
from helper.Audio import Audio
from helper.BluetoothHelper import BluetoothHelper
from helper.SystemHelper import System

bluetooth_helper = BluetoothHelper()
system_helper = System()
audio_helper = Audio()

class Tabs:
    taskbar: Taskbar = None
    radio_tab: RadioTab = None
    bluetooth_tab: BluetoothTab = None
    settings_tab: SettingsTab = None

    def __init__(self, taskbar: Taskbar, radio_tab: RadioTab, bluetooth_tab: BluetoothTab, soundboard_tab: SoundboardTab, settings_tab: SettingsTab):
        self.taskbar = taskbar
        self.radio_tab = radio_tab
        self.bluetooth_tab = bluetooth_tab
        self.soundboard_tab = soundboard_tab
        self.settings_tab = settings_tab

    def change_tab(self, e):
        index = e.control.selected_index
        self.radio_tab.get_song_info().update()

        self.radio_tab.hide()
        self.bluetooth_tab.hide()
        self.soundboard_tab.hide()
        self.settings_tab.hide()

        if index == 0:
            self.switch_radio_tab()

        if index == 1:
            self.switch_bluetooth_tab()

        if index == 2:
            if system_helper.is_party_mode():
                self.switch_soundboard_tab()
            else:
                self.switch_settings_tab()

        if index == 3:
            self.settings_tab.show()

    def switch_radio_tab(self):
        if bluetooth_helper.is_discovery_on():
            self.bluetooth_tab.get_btn_toggle().toggle_bluetooth_discovery()

        bluetooth_helper.disconnect()
        bluetooth_helper.turn_off()

        self.bluetooth_tab.device_connected.reset_connected_device()
        self.radio_tab.show()
        self.radio_tab.update()
        self.taskbar.update()

    def switch_bluetooth_tab(self):
        audio_helper.pause()
        bluetooth_helper.turn_on()

        self.taskbar.update()

        self.bluetooth_tab.get_device_connected().reset_connected_device()
        self.bluetooth_tab.show()

        self.radio_tab.get_grid().disable_indicator()

    def switch_soundboard_tab(self):
        self.soundboard_tab.show()

    def switch_settings_tab(self):
        self.settings_tab.show()
