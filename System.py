import os


class System:
    def shutdown_system(self):
        os.system('sudo shutdown now')

    def restart_system(self):
        os.system('sudo reboot')
