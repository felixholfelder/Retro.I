import os
from Strip import Strip

class System:
    strip = Strip()

    def shutdown_system(self, _):
        self.strip.disable()
        os.system('sudo shutdown now')

    def restart_system(self, _):
        self.strip.disable()
        os.system('sudo reboot')
    
    def pwd(self):
        return "/home/pi/Desktop/Retro.I"
