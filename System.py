import os

class System:
    # strip = Strip()

    def shutdown_system(self, _):
        # self.strip.disable()
        os.system('sudo shutdown now')

    def restart_system(self, _):
        # self.strip.disable()
        os.system('sudo reboot')
    
    def pwd(self):
        return "D:/SWE/Python/flet-gui"
