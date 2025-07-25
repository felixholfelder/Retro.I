import flet as ft

from components.SettingsButton import SettingsButton
from components.dialogs.SettingsBrightnessDialog import SettingsBrightnessDialog
from components.dialogs.SettingsCreditsDialog import SettingsCreditsDialog
from components.dialogs.SettingsLedDialog import SettingsLedDialog
from components.dialogs.SettingsInfoDialog import SettingsInfoDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from helper.Sounds import Sounds

sounds = Sounds()


class SettingsTab:
    tab = None

    shutdown_dialog: SettingsShutdownDialog = None
    led_dialog: SettingsLedDialog = None
    brightness_dialog: SettingsBrightnessDialog = None
    info_dialog: SettingsInfoDialog = None
    credits_dialog: SettingsCreditsDialog = None

    def __init__(self):
        self.shutdown_dialog = SettingsShutdownDialog()
        self.led_dialog = SettingsLedDialog()
        self.brightness_dialog = SettingsBrightnessDialog()
        self.info_dialog = SettingsInfoDialog()
        self.credits_dialog = SettingsCreditsDialog()
        
        self.tab = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Einstellungen", size=24),
                    ft.GridView(
                        expand=True,
                        runs_count=5,
                        max_extent=150,
                        child_aspect_ratio=1.0,
                        spacing=20,
                        run_spacing=50,
                        controls=[
                            SettingsButton().get(ft.icons.POWER_SETTINGS_NEW, "Radio ausschalten", lambda e: self.shutdown_dialog.open()),
                            SettingsButton().get(ft.icons.COLOR_LENS, "LED-Streifen", lambda e: self.led_dialog.open()),
                            SettingsButton().get(ft.icons.SETTINGS_DISPLAY_ROUNDED, "Helligkeit", lambda e: self.brightness_dialog.open()),
                            SettingsButton().get(ft.icons.INFO, "Info", lambda e: self.info_dialog.open()),
                            SettingsButton().get(ft.icons.STAR, "Credits", lambda e: self.credits_dialog.open()),
                        ]
                    ),
                    # ft.ListView(
                    #     [
                    #         SettingsButton().get(ft.icons.POWER_SETTINGS_NEW, "Radio ausschalten", lambda e: self.shutdown_dialog.open()),
                    #         SettingsButton().get(ft.icons.COLOR_LENS, "LED-Streifen", lambda e: self.led_dialog.open()),
                    #         SettingsButton().get(ft.icons.SETTINGS_DISPLAY_ROUNDED, "Helligkeit", lambda e: self.brightness_dialog.open()),
                    #         SettingsButton().get(ft.icons.INFO, "Info", lambda e: self.info_dialog.open()),
                    #         SettingsButton().get(ft.icons.STAR, "Credits", lambda e: self.credits_dialog.open()),
                    #     ],
                    #     spacing=10,
                    #     padding=20,
                    # )
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
