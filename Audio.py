import alsaaudio as audio


class Audio:
    def mixer(self):
        return audio.Mixer()

    def update_sound(self, value):
        self.mixer().setvolume(value)

    def mute(self):
        self.mixer().setmute(1)

    def unmute(self):
        self.mixer().setmute(0)

    def toggle_mute(self):
        if self.mixer().getmute() == 0:
            self.mute()
            return True
        self.unmute()
        return True
