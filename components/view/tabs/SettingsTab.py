import flet as ft

from components.SettingsButton import SettingsButton
from components.dialogs.SettingsCreditsDialog import SettingsCreditsDialog
from components.dialogs.SettingsInfoDialog import SettingsInfoDialog
from components.dialogs.SettingsLedDialog import SettingsLedDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from helper.Sounds import Sounds

sounds = Sounds()

class SettingsTab:
    tab = None

    shutdown_dialog = SettingsShutdownDialog()
    led_dialog = SettingsLedDialog()
    info_dialog = SettingsInfoDialog()
    credits_dialog = SettingsCreditsDialog()

    lv = ft.ListView(spacing=10, padding=20)
    lv.controls.append(SettingsButton().get(ft.icons.LOGOUT, "Radio ausschalten", shutdown_dialog.open()))
    lv.controls.append(SettingsButton().get(ft.icons.COLOR_LENS, "LED-Streifen", led_dialog.open()))
    lv.controls.append(SettingsButton().get(ft.icons.INFO, "Info", info_dialog.open()))
    lv.controls.append(SettingsButton().get(ft.icons.STAR, "Credits", credits_dialog.open()))

    def __init__(self):
        self.tab = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Einstellungen", size=24),
                    self.lv
                ]
            ),
            visible=False,
        )

    def update(self):
        self.tab.update()

    def get(self): return self.tab
    def get_dialogs(self): return [self.shutdown_dialog.get(), self.led_dialog.get(), self.info_dialog.get(), self.credits_dialog.get()]