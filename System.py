import os
import subprocess
from Strip import Strip
from Audio import Audio
from Constants import Constants
from datetime import datetime

audio_helper = Audio()
c = Constants()

class System:
    strip = Strip()
    is_party = "0"

    def shutdown_system(self, _):
        self.strip.disable()
        audio_helper.pause()
        audio_helper.shutdown_sound()
        os.system('sudo shutdown -h 0')

    def restart_system(self, _):
        self.strip.disable()
        audio_helper.pause()
        audio_helper.shutdown_sound()
        os.system('sudo reboot')
    
    def get_cpu_temp(self):
        line = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        temp = line[5:].strip()
        return temp
        
    def get_curr_date(self):
        return datetime.today().strftime('%d.%m.%Y')

    def get_img_path(self, img_src):
        return f"{c.pwd()}/assets/stations/{img_src}"
    
    def get_button_img_path(self):
        return f"{c.pwd()}/assets/buttons/SB_Green.png"
    
    def init_party_mode(self):
        self.is_party = os.environ.get("PARTY_MODE", "0")
    
    def is_party_mode(self):
        return self.is_party == "1"
