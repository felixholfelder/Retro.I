import flet as ft

from helper.AudioEffects import AudioEffects

audio_effects = AudioEffects()

class TaskbarPitch:
    ico = ft.Icon(name=ft.icons.HEIGHT, size=25)
    txt = ft.Text("", size=18)

    def update(self):
        self.txt.value = audio_effects.get_pitch_value()
        self.txt.update()

    def get(self):
        return ft.Row(self.ico, self.txt)
