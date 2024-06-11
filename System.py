import os
#from Strip import Strip

class System:
 #   strip = Strip()

    def shutdown_system(self, _):
  #      self.strip.disable()
        os.system('sudo shutdown now')

    def restart_system(self, _):
   #     self.strip.disable()
        os.system('sudo reboot')
    
    def pwd(self):
        return "D:/SWE/Python/Retro.I"


    def get_img_path(self, img_src):
        return f"{self.pwd()}/assets/stations/{img_src}"
