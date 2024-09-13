import threading
import time
import button
from multiprocessing import Process
import flet as ft
from adafruit_led_animation.color import BLUE, GREEN
from pyky040 import pyky040
from Audio import Audio
from BluetoothHelper import BluetoothHelper
from Constants import Constants
from Sounds import Sounds
from Stations import Stations
from Strip import Strip
from System import System
from WifiHelper import WifiHelper
from SoundCard import SoundCard
from ToastCard import ToastCard

# CLK=ORANGE
# DT=GELB
# SW=GRÜN
# +=BLAU
# -=LILA#

p = None

ICON_SIZE = 28

CLK_PIN = 13
DT_PIN = 6
SW_PIN = 5

VOLUME_STEP = 4

last_turn = 1

wifi_helper = WifiHelper()
bluetooth_helper = BluetoothHelper()
bluetooth_helper.turn_off()
audio_helper = Audio()
system_helper = System()
system_helper.init_party_mode()
stations_helper = Stations()
c = Constants()
sounds = Sounds()
strip = Strip()
strip.start()

bluetooth_helper.turn_on()
bluetooth_helper.bluetooth_discovery_off()
bluetooth_helper.turn_off()

txt_discovery_status = None
ico_discovery_status = None
btn_discovery_status = None

txt_device_connected = None
ico_device_connected = None
btn_device_connected = None

ssid = ""

wifi_connection_dialog_ssid = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
wifi_connection_dialog_pass = ft.TextField(password=True, autofocus=True, on_focus=lambda e: system_helper.open_keyboard(), on_blur=lambda e: system_helper.close_keyboard())
wifi_connection_dialog_btn = ft.FilledButton("Verbinden", on_click=lambda e: connect())

def connect():
    global ssid, p
    wifi_connection_dialog_btn.disabled = True
    wifi_connection_dialog_btn.text = "Wird verbunden..."
    wifi_not_connected(p)
    p.update()

    wifi_helper.connect_to_wifi(ssid, wifi_connection_dialog_pass.value)
    
    wifi_connection_dialog_pass.value = ""

    close_connection_dialog()
    wifi_connection_dialog_btn.disabled = False
    wifi_connection_dialog_btn.text = "Verbinden"
    update_taskbar(p)
    p.update()

wifi_connection_dialog = ft.AlertDialog(
    content=ft.Column(
        width=400,
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            wifi_connection_dialog_ssid,
            ft.Row([ft.Text("Passwort:", size=18), wifi_connection_dialog_pass]),
        ]
    ),
    actions=[wifi_connection_dialog_btn]
)

wifi_loading = ft.Text()
wifi_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
wifi_dialog = ft.AlertDialog(
    content=ft.Column(
        width=500,
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[wifi_loading, wifi_list]
    )
)

def open_connection_dialog(name):
    global ssid
    ssid = name
    
    wifi_connection_dialog_ssid.value = name
    wifi_connection_dialog.open = True
    p.update()

def close_connection_dialog():
    wifi_connection_dialog.open = False

def open_wifi_dialog():
    wifi_loading.value = "Netzwerke werden geladen..."
    wifi_list.controls = None
    wifi_dialog.open = True
    p.update()
    
    curr_ssid = wifi_helper.get_current_ssid()
    networks = wifi_helper.get_networks()
    
    for n in networks:
        ico = ft.Icon("done")
        btn = ft.TextButton(
            content=ft.Container(content=ft.Row(controls=[ico, ft.Text(n)])),
            on_click=lambda e, name=n: open_connection_dialog(name),
        )

        if (curr_ssid != n):
            ico.visible = False
        
        wifi_list.controls.append(btn)

    wifi_loading.value = ""
    p.update()

ico_wifi = ft.IconButton(alignment=ft.alignment.center_left, icon=ft.icons.WIFI, icon_color=ft.colors.BLACK, on_click=lambda e: open_wifi_dialog())
ico_bluetooth = ft.Icon(name=ft.icons.BLUETOOTH)

volume_icon = ft.Icon(name=ft.icons.VOLUME_UP_ROUNDED, color=ft.colors.BLACK)
volume_text = ft.Text(f"{audio_helper.get_volume()}%", size=18)

def wifi_not_connected(page: ft.Page):
    global ico_wifi
    ico_wifi.icon = ft.icons.WIFI_OFF_ROUNDED
    ico_wifi.icon_color = ft.colors.BLACK
    page.update()

def wifi_connected(page: ft.Page):
    global ico_wifi
    ico_wifi.icon = ft.icons.WIFI_ROUNDED
    ico_wifi.icon_color = ft.colors.GREEN
    page.update()

def update_taskbar(page: ft.Page):
    global ico_wifi, ico_bluetooth

    ico_wifi.icon_color = ft.colors.BLACK
    ico_bluetooth.color = ft.colors.BLACK

    if wifi_helper.is_connected():
        wifi_connected(page)
    else:
        wifi_not_connected(page)
    
    page.update()

    if bluetooth_helper.is_bluetooth_on():
        ico_bluetooth.name = ft.icons.BLUETOOTH_ROUNDED
        ico_bluetooth.color = ft.colors.BLACK
        if bluetooth_helper.is_discovery_on():
            ico_bluetooth.color = ft.colors.GREEN
        else:
            ico_bluetooth.color = ft.colors.BLACK

    else:
        ico_bluetooth.name = ft.icons.BLUETOOTH_DISABLED_ROUNDED

    if bluetooth_helper.get_device_name():
        ico_bluetooth.name = ft.icons.BLUETOOTH_CONNECTED_ROUNDED
        ico_bluetooth.color = ft.colors.GREEN

    page.update()

def update_taskbar_process(page: ft.Page):
    while True:
        update_taskbar(page)
        time.sleep(5)

def enable_discovery():
    bluetooth_helper.bluetooth_discovery_on()
    txt_discovery_status.value = "Bluetooth sichtbar"
    ico_discovery_status.name = ft.icons.BLUETOOTH
    btn_discovery_status.style.bgcolor = ft.colors.GREEN


def disable_discovery():
    bluetooth_helper.bluetooth_discovery_off()
    txt_discovery_status.value = "Bluetooth nicht sichtbar"
    ico_discovery_status.name = ft.icons.BLUETOOTH_DISABLED
    btn_discovery_status.style.bgcolor = ft.colors.RED


def toggle_bluetooth_discovery(page: ft.Page):
    discovery_on = bluetooth_helper.is_discovery_on()
    if discovery_on:
        disable_discovery()
    else:
        enable_discovery()
    page.update()


def update_connected_device(page):
    name = bluetooth_helper.get_device_name()
    if name != "":
        txt_device_connected.value = f"Verbunden mit: {name}"
        ico_device_connected.name = ft.icons.PHONELINK
        disable_discovery()
    else:
        txt_device_connected.value = "Kein Gerät verbunden"
        ico_device_connected.name = ft.icons.PHONELINK_OFF
    
    update_taskbar(page)
    page.update()


def bluetooth_listener(page):
    while True:
        update_connected_device(page)
        time.sleep(10)


def update_sound(value, page: ft.Page):
    global volume_text
    if not audio_helper.is_mute():
        audio_helper.update_sound(value)
        strip.update_sound_strip(value)
        volume_text.value = f"{audio_helper.get_volume()}%"
        page.update()


def inc_sound(page: ft.Page):
    global last_turn
    if last_turn == 1:
        value = audio_helper.get_volume() + VOLUME_STEP
        if value >= 0 and value <= 100:
            update_sound(value, page)
    last_turn = 1


def dec_sound(page: ft.Page):
    global last_turn
    if last_turn == 0:
        value = audio_helper.get_volume() - VOLUME_STEP
        if value >= 0 and value <= 100:
            update_sound(value, page)
    last_turn = 0


def toggle_mute(page: ft.Page):
    global volume_icon, volume_text
    is_mute = audio_helper.toggle_mute()
    strip.toggle_mute(is_mute)

    if is_mute:
        volume_icon.name=ft.icons.VOLUME_OFF_ROUNDED
        volume_icon.color=ft.colors.RED
        volume_text.value = ""
    else:
        volume_icon.name=ft.icons.VOLUME_UP_ROUNDED
        volume_icon.color=ft.colors.BLACK
        volume_text.value = f"{audio_helper.get_volume()}%"

    page.update()


def get_station_by_image(src):
    for i, obj in enumerate(stations_helper.load_radio_stations()):
        if system_helper.get_img_path(obj["logo"]) == src:
            return [i, obj]
    return -1


indicator_refs = []


def disable_indicator():
    for ref in indicator_refs:
        ref.current.visible = False


def toggle_indicator(index):
    disable_indicator()
    indicator_refs[index].current.visible = True


def change_radio_station(station, index, page):
    global strip_color
    color = station["color"]

    toggle_indicator(index)
    page.theme.color_scheme_seed = color
    page.navigation_bar.bgcolor = color
    audio_helper.play(station["src"])
    strip.update_strip(color)
    page.update()


def start_rotary(page: ft.Page):
    rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
    rotary.setup(step=VOLUME_STEP,
                 inc_callback=lambda e: inc_sound(page), dec_callback=lambda e: dec_sound(page),
                 sw_callback=lambda: toggle_mute(page))
    rotary_thread = threading.Thread(target=rotary.watch)
    rotary_thread.start()


def main(page: ft.Page):
    global p, txt_discovery_status, ico_discovery_status, btn_discovery_status, txt_device_connected, ico_device_connected, btn_device_connected, ico_wifi, ico_bluetooth, volume_icon, volume_text, wifi_dialog, wifi_connection_dialog
    start_rotary(page)
    #page.window_full_screen = True
    page.window_maximized = True
    page.window_frameless = True
    page.theme = ft.Theme(
        color_scheme_seed='green',
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.GREY_500,
                ft.MaterialState.DEFAULT: ft.colors.GREY_400,
            },
            thickness=40,
            radius=20,
        )
    )
    page.add(audio_helper.init())
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.title = "Retro.I"
    
    page.add(wifi_dialog)
    page.add(wifi_connection_dialog)

    page.appbar = ft.AppBar(
        title=ft.Row([
            volume_icon,
            volume_text
        ]),
        bgcolor=ft.colors.SURFACE_VARIANT,
        toolbar_height=32,
        actions=[ico_wifi, ico_bluetooth],
    )

    page.update()
    
    update_taskbar(page)

    def change_tab(e):
        index = e.control.selected_index
        if index == 0:
            switch_radio_tab()
            bluetooth_helper.turn_off()
            update_taskbar(page)
        else:
            radio_tab.visible = False

        if index == 1:
            switch_bluetooth_tab()
            disable_indicator()
            bluetooth_helper.turn_on()
            update_taskbar(page)
        else:
            bluetooth_tab.visible = False

        if system_helper.is_party_mode():
            if index == 2:
                switch_soundboard_tab()
                disable_indicator()
            else:
                soundboard_tab.visible = False

            if index == 3:
                settings_tab.visible = True
            else:
                settings_tab.visible = False
        else:
            if index == 2:
                settings_tab.visible = True
            else:
                settings_tab.visible = False

        page.update()

    def switch_radio_tab():
        if bluetooth_helper.is_discovery_on():
            toggle_bluetooth_discovery(page)
        bluetooth_helper.disconnect()
        strip.fill(GREEN)
        update_connected_device(page)
        radio_tab.visible = True

    def switch_bluetooth_tab():
        audio_helper.pause()
        strip.fill(BLUE)
        update_connected_device(page)
        bluetooth_tab.visible = True

    def switch_soundboard_tab():
        soundboard_tab.visible = True

    destinations = []
    destinations.append(
        ft.NavigationDestination(
            label="Radiosender",
            icon_content=ft.Icon(ft.icons.RADIO_OUTLINED, size=ICON_SIZE),
            selected_icon_content=ft.Icon(ft.icons.RADIO, size=ICON_SIZE)
        )
    )

    destinations.append(
        ft.NavigationDestination(
            label="Bluetooth",
            icon_content=ft.Icon(ft.icons.BLUETOOTH_OUTLINED, size=ICON_SIZE),
            selected_icon_content=ft.Icon(ft.icons.BLUETOOTH, size=ICON_SIZE)
        )
    )

    if system_helper.is_party_mode():
        destinations.append(
            ft.NavigationDestination(
                label="Soundboard",
                icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD_OUTLINED, size=ICON_SIZE),
                selected_icon_content=ft.Icon(ft.icons.SPACE_DASHBOARD, size=ICON_SIZE)
            ),
        )

    destinations.append(
        ft.NavigationDestination(
            label="Einstellungen",
            icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED, size=ICON_SIZE),
            selected_icon_content=ft.Icon(ft.icons.SETTINGS, size=ICON_SIZE),
        )
    )

    nav = ft.NavigationBar(
        bgcolor="green",
        on_change=change_tab,
        selected_index=0,
        destinations=destinations
    )
    page.navigation_bar = nav

    grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=50
    )

    soundboard_grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        spacing=80,
        run_spacing=50
    )

    dlg = ft.AlertDialog(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=75,
                    controls=[
                        ft.Column(
                            [ft.IconButton(ft.icons.POWER_OFF, icon_size=75, on_click=system_helper.shutdown_system),
                             ft.Text("Ausschalten", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=16))],
                            alignment=ft.MainAxisAlignment.CENTER),
                        ft.Column([ft.IconButton(ft.icons.REPLAY, icon_size=75, on_click=system_helper.restart_system),
                                   ft.Text("Neustarten", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=16))],
                                  alignment=ft.MainAxisAlignment.CENTER),
                    ]
                )
            ]
        )
    )
    page.add(dlg)

    dlg_led = ft.AlertDialog(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Switch("LED-Streifen ausschalten", label_style=ft.TextStyle(size=20),
                          on_change=lambda e: strip.toggle_strip(), value=strip.is_strip_active()),
                ft.Divider(),
                ft.Row([
                    ft.Text("Helligkeit", style=ft.TextStyle(size=20)),
                    ft.Slider(on_change=strip.change_brightness, min=0, max=100, value=strip.get_curr_brightness(),
                              width=420)
                ])
            ]
        )
    )
    page.add(dlg_led)

    dlg_credits = ft.AlertDialog(
        content=ft.Column(
            width=500,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Retro.i", weight=ft.FontWeight.BOLD, size=28),
                ft.Divider(),
                ft.Text("Klasse: FWI1 2023/2024", weight=ft.FontWeight.BOLD, size=20),
                ft.Text("Felix Holfelder", size=20),
                ft.Text("Dominik Schelter", size=20),
                ft.Text("Johannes Lehner", size=20),
                ft.Text("Yannick Grübl", size=20),
                ft.Divider(),
                ft.Text("Besonderen Dank an:", weight=ft.FontWeight.BOLD, size=22),
                ft.Text("Goldschmiede und Uhren Gruhle", size=20),
                ft.Text("Klaus Schelter", size=20),
            ]
        )
    )
    page.add(dlg_credits)

    cpu_text = ft.TextSpan(system_helper.get_cpu_temp(), style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    dlg_info = ft.AlertDialog(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            width=500,
            tight=True,
            controls=[
                ft.Text(spans=[ft.TextSpan("CPU-Temperatur: "), cpu_text], size=20),
                ft.Divider(),
                ft.Text(f"Datum: {system_helper.get_curr_date()}", size=20),
            ]
        )
    )
    page.add(dlg_info)

    def show_dialog(_):
        dlg.open = True
        page.update()

    def show_led_dialog(_):
        dlg_led.open = True
        page.update()

    def show_credits_dialog(_):
        dlg_credits.open = True
        page.update()

    def show_info_dialog(_):
        dlg_info.open = True
        cpu_text.value = f"CPU-Temperatur: {system_helper.get_cpu_temp()}"
        page.update()

    lv = ft.ListView(spacing=10, padding=20)
    lv.controls.append(ft.TextButton(height=100, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[ft.Icon(ft.icons.LOGOUT),
                                                                          ft.Text("Radio ausschalten",
                                                                                  style=ft.TextStyle(size=20))]),
                                     on_click=show_dialog))
    lv.controls.append(ft.TextButton(height=100, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[ft.Icon(ft.icons.COLOR_LENS),
                                                                          ft.Text("LED-Streifen",
                                                                                  style=ft.TextStyle(size=20))]),
                                     on_click=show_led_dialog))
    lv.controls.append(ft.TextButton(height=100, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[ft.Icon(ft.icons.INFO), ft.Text("Info",
                                                                                                          style=ft.TextStyle(
                                                                                                              size=20))]),
                                     on_click=show_info_dialog))
    lv.controls.append(ft.TextButton(height=100, content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[ft.Icon(ft.icons.STAR), ft.Text("Credits",
                                                                                                          style=ft.TextStyle(
                                                                                                              size=20))]),
                                     on_click=show_credits_dialog))

    for i in range(len(stations_helper.load_radio_stations())):
        indicator_refs.append(ft.Ref[ft.Image]())
        station = stations_helper.load_radio_stations()[i]
        grid.controls.append(
            ft.Stack(
                alignment=ft.MainAxisAlignment.END,
                fit=ft.StackFit.EXPAND,
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.GREY_200,
                        on_click=lambda e, index=i, src=station: change_radio_station(src, index, page),
                        border_radius=10,
                        content=ft.Image(src=system_helper.get_img_path(station["logo"]), border_radius=ft.border_radius.all(4)),
                        padding=10,
                    ),
                    ft.Image(ref=indicator_refs[i], src=f"{c.pwd()}/assets/party.gif", opacity=0.7, visible=False)
                ]
            )
        )

    # Card for toast (drinking)
    soundboard_grid.controls.append(ToastCard.get(page, i))

    for i in range(len(sounds.load_sounds())):
        sound = sounds.load_sounds()[i]
        soundboard_grid.controls.append(SoundCard.get(page, sound["src"], sound["name"], i))

    ico_discovery_status = ft.Icon(ft.icons.BLUETOOTH_DISABLED)
    txt_discovery_status = ft.Text("Bluetooth nicht sichtbar", style=ft.TextStyle(size=20))

    btn_discovery_status = ft.FilledButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ico_discovery_status,
                txt_discovery_status
            ],
        ),
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED,
        ),
        width=500,
        height=80,
        on_click=lambda e: toggle_bluetooth_discovery(page),
    )

    ico_device_connected = ft.Icon(ft.icons.PHONELINK_OFF)
    txt_device_connected = ft.Text("Kein Gerät verbunden", style=ft.TextStyle(size=20))

    btn_device_connected = ft.TextButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ico_device_connected,
                txt_device_connected
            ],
        ),
        width=500,
        height=80,
        on_click=lambda e: update_connected_device(page),
    )

    # Tabs
    radio_tab = ft.Container(
        content=ft.Column([
            ft.Row([grid]),
        ]),
        margin=ft.margin.only(right=75),
    )

    bluetooth_tab = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            spacing=50,
            controls=[
                btn_discovery_status,
                btn_device_connected
            ]
        ),
        visible=False,
    )

    soundboard_tab = ft.Container(
        content=ft.Column([ft.Row([soundboard_grid])]),
        visible=False,
        margin=ft.margin.only(right=75, bottom=75),
    )

    settings_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Einstellungen", size=24),
                lv
            ]
        ),
        visible=False,
    )

    tabs = []
    tabs.append(radio_tab)
    tabs.append(bluetooth_tab)
    tabs.append(settings_tab)

    if system_helper.is_party_mode():
        tabs.append(soundboard_tab)

    page.add(
        ft.Column(tabs)
    )
    page.update()
    
    p = page
    p.update()

    audio_helper.startup_sound()

    bluetooth_process = threading.Thread(target=bluetooth_listener(page))
    bluetooth_process.start()

    taskbar_process = threading.Thread(target=update_taskbar_process(page))
    taskbar_process.start()


ft.app(main)
