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

    def __init__(self):
        self.tab = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Einstellungen", size=24),
                    ft.ListView(
                        [
                            SettingsButton().get(ft.icons.LOGOUT, "Radio ausschalten", self.shutdown_dialog.open),
                            SettingsButton().get(ft.icons.COLOR_LENS, "LED-Streifen", self.led_dialog.open),
                            SettingsButton().get(ft.icons.INFO, "Info", self.info_dialog.open),
                            SettingsButton().get(ft.icons.STAR, "Credits", self.credits_dialog.open),
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

    def get_dialogs(self): return [self.shutdown_dialog.get(), self.led_dialog.get(), self.info_dialog.get(), self.credits_dialog.get()]
