import os
import re
import subprocess


class WifiHelper:
    def is_connected(self):
        ip = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
        return ip != ""

    def get_networks(self):
        networks = os.popen("sudo iwlist wlan0 scanning | grep ESSID").read()
        networkslist = re.findall(r'"(.+?)"', networks)
        return list(dict.fromkeys(networkslist))

    def connect_to_wifi(self, ssid, password):
        if password == "":
            command = ["nmcli", "d", "wifi", "connect", ssid]
        else:
            command = ["nmcli", "d", "wifi", "connect", ssid, "password", password]

        subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
