from subprocess import check_output


class WifiHelper:
    def is_connected(self):
        wifi_ip = check_output(['hostname', '-I'])
        print(wifi_ip)
        return wifi_ip is not None