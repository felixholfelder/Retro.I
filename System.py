import os


class System:
    def shutdown_system(self, _):
        os.system('sudo shutdown now')

    def restart_system(self, _):
        os.system('sudo reboot')
    
    def pwd(self):
        return "/home/pi/Desktop/Retro.I"
