import os
from Strip import Strip
from Audio import Audio
from Constants import Constants

audio_helper = Audio()
c = Constants()

class System:
    strip = Strip()

    def shutdown_system(self, _):
        self.strip.disable()
        audio_helper.shutdown_sound()
        os.system('sudo shutdown now')

    def restart_system(self, _):
        self.strip.disable()
        audio_helper.shutdown_sound()
        os.system('sudo reboot')

    def get_img_path(self, img_src):
        return f"{c.pwd()}/assets/stations/{img_src}"
    
    def get_button_img_path(self):
        return f"{c.pwd()}/assets/buttons/SB_Green.png"
