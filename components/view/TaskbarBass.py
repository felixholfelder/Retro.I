import flet as ft

from helper.AudioEffects import AudioEffects

audio_effects = AudioEffects()

class TaskbarBass:
    ico = ft.Icon(name=ft.icons.SURROUND_SOUND, size=25)
    txt = ft.Text("", size=18)

    def update(self):
        self.txt.value = f"+{audio_effects.get_bass_value()}dB" if audio_effects.get_bass_value() >= 0 else f"-{audio_effects.get_bass_value()}dB"
        self.txt.update()

    def get(self):
        return ft.Row(self.ico, self.txt)
