import os


class System:
    def shutdown_system(_):
        os.system('sudo shutdown now')

    def restart_system(_):
        os.system('sudo reboot')
