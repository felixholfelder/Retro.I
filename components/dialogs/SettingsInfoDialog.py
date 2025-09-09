import flet as ft

from helper.SystemHelper import SystemHelper

system_helper = SystemHelper()


class SettingsInfoDialog(ft.AlertDialog):
    cpu_temp_text = ft.TextSpan("")
    ssid_text = ft.TextSpan("")
    ip_text = ft.TextSpan("")
    hostname_text = ft.TextSpan("")
    subnetmask_text = ft.TextSpan("")
    mac_text = ft.TextSpan("")
    gateway_text = ft.TextSpan("")
    dns_pri_text = ft.TextSpan("")
    dns_sec_text = ft.TextSpan("")

    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            width=500,
            tight=True,
            controls=[
                ft.ListView(
                    controls=[
                        ft.Text("Allgemein", weight=ft.FontWeight.BOLD, size=28),
                        ft.Text(spans=[ft.TextSpan("Datum: "), ft.TextSpan(system_helper.get_curr_date())], size=20),
                        ft.Text(spans=[ft.TextSpan("CPU-Temperatur: "), self.cpu_temp_text], size=20),
                        ft.Divider(),
                        ft.Text("IP-Config", weight=ft.FontWeight.BOLD, size=28),
                        ft.Text(spans=[ft.TextSpan("SSID: "), self.ip_text], size=20),
                        ft.Text(spans=[ft.TextSpan("IP-Adresse: "), self.ip_text], size=20),
                        ft.Text(spans=[ft.TextSpan("Hostname: "), self.hostname_text], size=20),
                        ft.Text(spans=[ft.TextSpan("Subnetzmaske: "), self.subnetmask_text], size=20),
                        ft.Text(spans=[ft.TextSpan("MAC-Adresse: "), self.mac_text], size=20),
                        ft.Text(spans=[ft.TextSpan("Gateway: "), self.gateway_text], size=20),
                        ft.Text(spans=[ft.TextSpan("DNS Primär: "), self.dns_pri_text], size=20),
                        ft.Text(spans=[ft.TextSpan("DNS Sekundär: "), self.dns_sec_text], size=20)
                    ]
                )
            ]
        )

    def open_dialog(self):
        self.cpu_temp_text.text = system_helper.get_cpu_temp()
        self.cpu_temp_text.update()
        self.update_ip_config()
        self.open = True
        self.update()

    def update_ip_config(self):
        ip_config = system_helper.get_network_config()

        self.ssid_text.text = ip_config["ssid"] or ""
        self.ip_text.text = ip_config["ip"] or ""
        self.hostname_text.text = ip_config["hostname"] or ""
        self.subnetmask_text.text = ip_config["subnetmask"] or ""
        self.mac_text.text = ip_config["mac_address"] or ""
        self.gateway_text.text = ip_config["gateway"] or ""
        self.dns_pri_text.text = ip_config["dns"][0] or ""
        self.dns_sec_text.text = ip_config["dns"][1] or ""

        self.ssid_text.update()
        self.ip_text.update()
        self.hostname_text.update()
        self.subnetmask_text.update()
        self.mac_text.update()
        self.gateway_text.update()
        self.dns_pri_text.update()
        self.dns_sec_text.update()
