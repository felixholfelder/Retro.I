import flet as ft

from helper.PageState import PageState
from helper.SystemHelper import SystemHelper
from helper.WifiHelper import WifiHelper

system_helper = SystemHelper()

class SettingsInfoDialog:
    dialog = None
    
    cpu_temp_text = ft.TextSpan("")
    
    ip_text = ft.TextSpan("")
    hostname_text = ft.TextSpan("")
    subnetmask_text = ft.TextSpan("")
    mac_text = ft.TextSpan("")
    gateway_text = ft.TextSpan("")
    dns_pri_text = ft.TextSpan("")
    dns_sec_text = ft.TextSpan("")

    def __init__(self):
        self.dialog = ft.AlertDialog(
            content=ft.Container(
                width=500,
                content=ft.ListView(
                    expand=True,
                    controls=[
                        ft.Text("Allgemein", weight=ft.FontWeight.BOLD, size=28),
                        ft.Text(spans=[ft.TextSpan("Datum: "), ft.TextSpan(system_helper.get_curr_date())], size=20),
                        ft.Text(spans=[ft.TextSpan("CPU-Temperatur: "), self.cpu_temp_text], size=20),
                        ft.Divider(),
                        ft.Text("IP-Config", weight=ft.FontWeight.BOLD, size=28),
                        ft.Text(spans=[ft.TextSpan("IP-Adresse: "), self.ip_text], size=20),
                        ft.Text(spans=[ft.TextSpan("Hostname: "), self.hostname_text], size=20),
                        ft.Text(spans=[ft.TextSpan("Subnetzmaske: "), self.subnetmask_text], size=20),
                        ft.Text(spans=[ft.TextSpan("MAC-Adresse: "), self.mac_text], size=20),
                        ft.Text(spans=[ft.TextSpan("Gateway: "), self.gateway_text], size=20),
                        ft.Text(spans=[ft.TextSpan("DNS Primär: "), self.dns_pri_text], size=20),
                        ft.Text(spans=[ft.TextSpan("DNS Sekundär: "), self.dns_sec_text], size=20)
                    ]
                )
            )
        )
        PageState.page.add(self.dialog)

    def open(self):
        self.cpu_temp_text.text = system_helper.get_cpu_temp()
        self.cpu_temp_text.update()
        self.update_ip_config()
        self.dialog.open = True
        self.dialog.update()
        
    def update_ip_config(self):
        ip_config = system_helper.get_network_config()
        
        self.ip_text.text = ip_config["ip"] or ""
        self.hostname_text.text = ip_config["hostname"] or ""
        self.subnetmask_text.text = ip_config["subnetmask"] or ""
        self.mac_text.text = ip_config["mac_address"] or ""
        self.gateway_text.text = ip_config["gateway"] or ""
        self.dns_pri_text.text = ip_config["dns"][0] or ""
        self.dns_sec_text.text = ip_config["dns"][1] or ""
        
        self.ip_text.update()
        self.hostname_text.update()
        self.subnetmask_text.update()
        self.mac_text.update()
        self.gateway_text.update()
        self.dns_pri_text.update()
        self.dns_sec_text.update()
