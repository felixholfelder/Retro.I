import os
import time
import subprocess
import keyboard
from helper.Strip import Strip
from helper.Audio import Audio
from helper.Constants import Constants
from datetime import datetime

audio_helper = Audio()
c = Constants()

class System:
    strip = Strip()
    is_party = "0"
    
    def __init__(self):
        self.init_party_mode()

    def shutdown_system(self, _):
        audio_helper.shutdown_sound()
        self.strip.disable()
        time.sleep(3)
        os.system('sudo shutdown -h 0')

    def restart_system(self, _):
        audio_helper.shutdown_sound()
        self.strip.disable()
        time.sleep(3)
        os.system('sudo reboot')
    
    def stopp_app(self, _):
        keyboard.send('alt', 'F4')
    
    def get_cpu_temp(self):
        line = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        temp = line[5:].strip()
        return temp
        
    def get_curr_date(self):
        return datetime.today().strftime('%d.%m.%Y')

    def get_img_path(self, img_src):
        if "http" in img_src:
            return img_src

        return f"{c.pwd()}/assets/stations/{img_src}"
    
    def get_button_img_path(self):
        return f"{c.pwd()}/assets/buttons/SB_Green.png"
    
    def init_party_mode(self):
        self.is_party = os.environ.get("PARTY_MODE", "0")
    
    def is_party_mode(self):
        return self.is_party == "1"
    
    def open_keyboard(self):
        self.close_keyboard()
        os.system("wvkbd-mobintl -L 300")
    
    def close_keyboard(self):
        os.system("pkill wvkbd-mobintl")
