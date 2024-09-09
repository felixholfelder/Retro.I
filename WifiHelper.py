import subprocess


class WifiHelper:
    def is_connected(self):
        ip = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        return ip != ""
