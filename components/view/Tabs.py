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

    def change_tab(self, index):
        # index = e.control.selected_index
        self.radio_tab.get_song_info().update()

        if index == 0:
            self.switch_radio_tab()
            bluetooth_helper.turn_off()
            self.taskbar.update()
        else:
            self.radio_tab.visible = False
            self.radio_tab.get_song_info().reset()

        if index == 1:
            self.switch_bluetooth_tab()
            self.radio_tab.get_grid().disable_indicator()
            bluetooth_helper.turn_on()
            self.taskbar.update()
        else:
            self.bluetooth_tab.visible = False

        if system_helper.is_party_mode():
            if index == 2:
                self.switch_soundboard_tab()
                self.radio_tab.get_grid().disable_indicator()
            else:
                self.soundboard_tab.visible = False

            if index == 3:
                self.settings_tab.visible = True
            else:
                self.settings_tab.visible = False
        else:
            if index == 2:
                self.settings_tab.visible = True
            else:
                self.settings_tab.visible = False

        self.radio_tab.update()
        self.bluetooth_tab.update()
        self.soundboard_tab.update()
        self.settings_tab.update()

    def switch_radio_tab(self):
        if bluetooth_helper.is_discovery_on():
            self.bluetooth_tab.get_btn_toggle().toggle_bluetooth_discovery()
        bluetooth_helper.disconnect()
        self.bluetooth_tab.device_connected.reset_connected_device()
        self.radio_tab.get().visible = True
        self.radio_tab.update()

    def switch_bluetooth_tab(self):
        audio_helper.pause()
        self.bluetooth_tab.get_device_connected().reset_connected_device()
        self.bluetooth_tab.get().visible = True
        self.bluetooth_tab.update()

    def switch_soundboard_tab(self):
        self.soundboard_tab.get().visible = True
        self.soundboard_tab.update()
