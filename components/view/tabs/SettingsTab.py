import flet as ft

from components.SettingsButton import SettingsButton
from components.dialogs.SettingsCreditsDialog import SettingsCreditsDialog
from components.dialogs.SettingsLedDialog import SettingsLedDialog
from components.dialogs.SettingsInfoDialog import SettingsInfoDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from helper.Sounds import Sounds

sounds = Sounds()


class SettingsTab:
    tab = None

    shutdown_dialog = SettingsShutdownDialog()
    led_dialog = SettingsLedDialog()
    info_dialog = SettingsInfoDialog()
    credits_dialog = SettingsCreditsDialog()

    def __init__(self):
        self.tab = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Einstellungen", size=24),
                    ft.ListView(
                        [
                            SettingsButton().get(ft.icons.POWER_SETTINGS_NEW, "Radio ausschalten", lambda e: self.shutdown_dialog.open()),
                            SettingsButton().get(ft.icons.COLOR_LENS, "LED-Streifen", lambda e: self.led_dialog.open()),
                            SettingsButton().get(ft.icons.INFO, "Info", lambda e: self.info_dialog.open()),
                            SettingsButton().get(ft.icons.STAR, "Credits", lambda e: self.credits_dialog.open()),
                        ],
                        spacing=10,
                        padding=20)
                ]
            ),
            visible=False,
        )

    def update(self):
        self.tab.update()

    def show(self):
        self.tab.visible = True
        self.update()

    def hide(self):
        self.tab.visible = False
        self.update()

    def get(self): return self.tab
