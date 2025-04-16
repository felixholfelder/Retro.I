import flet as ft

from helper.Audio import Audio

audio_helper = Audio()

class TaskbarVolume:
    ico_volume = ft.Icon(name=ft.icons.VOLUME_UP_ROUNDED, size=25)
    txt_volume = ft.Text("", size=18)

    def update(self):
        self.ico_volume.name = ft.icons.VOLUME_OFF_ROUNDED if audio_helper.is_mute() else ft.icons.VOLUME_UP_ROUNDED
        self.ico_volume.color = ft.colors.RED if audio_helper.is_mute() else ft.colors.BLACK
        self.ico_volume.update()
        self.txt_volume.value = f"{audio_helper.get_volume()}%" if not audio_helper.is_mute() else ""
        self.txt_volume.update()

    def get(self):
        return [self.ico_volume, self.txt_volume]
