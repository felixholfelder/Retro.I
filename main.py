import threading
import time

from helper.dialogs.StationDeleteDialog import StationDeleteDialog
from scripts import button
from multiprocessing import Process
import flet as ft
from adafruit_led_animation.color import BLUE, GREEN
from pyky040 import pyky040
from helper.Audio import Audio
from helper.BluetoothHelper import BluetoothHelper
from helper.Constants import Constants
from helper.Sounds import Sounds
from helper.Stations import Stations
from helper.Strip import Strip
from helper.System import System
from helper.WifiHelper import WifiHelper
from helper.RadioHelper import RadioHelper
from components.SoundCard import SoundCard
from components.ToastCard import ToastCard
from components.GpioButton import GpioButton
from components.SettingsButton import SettingsButton

# CLK=ORANGE
# DT=GELB
# SW=GRÜN
# +=BLAU
# -=LILA#

p = None

ICON_SIZE = 28

SW_PIN = 5
DT_PIN = 6
CLK_PIN = 13

VOLUME_STEP = 4

last_turn = 1

tab_index = 0

wifi_helper = WifiHelper()
radio_helper = RadioHelper()
bluetooth_helper = BluetoothHelper()
bluetooth_helper.turn_off()
audio_helper = Audio()
system_helper = System()
system_helper.init_party_mode()
stations_helper = Stations()
constants = Constants()
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

radio_grid = ft.GridView(
    expand=True,
    runs_count=5,
    max_extent=150,
    child_aspect_ratio=1.0,
    spacing=20,
    run_spacing=50
)


def delete_dialog():
    stations_helper.delete_station(constants.current_station_index_to_delete)
    reload_radio_stations(p)


def open_delete_station_dialog(index):
    constants.current_station_index_to_delete = index
    station_delete_dialog.open()


station_delete_dialog = StationDeleteDialog(delete_dialog(), p).get()

def reload_radio_stations(page):
    radio_grid.controls = []
    constants.indicator_refs = []

    for i, station in enumerate(stations_helper.load_radio_stations()):
        constants.indicator_refs.append(ft.Ref[ft.Image]())
        radio_grid.controls.append(
            ft.Stack(
                alignment=ft.MainAxisAlignment.END,
                fit=ft.StackFit.EXPAND,
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.GREY_200,
                        on_click=lambda e, index=i, src=station: change_radio_station(src, page, index),
                        on_long_press=lambda e, index=i: open_delete_station_dialog(index),
                        border_radius=10,
                        # TODO - expand???
                        content=ft.Image(src=system_helper.get_img_path(station["logo"]),
                                         border_radius=ft.border_radius.all(4)) if station["logo"] != "" else ft.Text(
                            station["name"], text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, expand=True),
                        padding=10,
                    ),
                    ft.Image(ref=constants.indicator_refs[i], src=f"{constants.pwd()}/assets/party.gif", opacity=0.7,
                             visible=False)
                ]
            )
        )
    page.update()

ssid = ""

wifi_connection_dialog_ssid = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
wifi_connection_dialog_pass = ft.TextField(password=True, autofocus=True,
                                           on_focus=lambda e: system_helper.open_keyboard(),
                                           on_blur=lambda e: system_helper.close_keyboard())
wifi_connection_dialog_btn = ft.FilledButton("Verbinden", on_click=lambda e: connect())


def connect():
    global ssid
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
wifi_list = ft.ListView(spacing=10, padding=20, expand=True)
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
    p.update()


def open_wifi_dialog():
    wifi_loading.value = "Netzwerke werden geladen..."
    wifi_list.controls = None
    wifi_dialog.open = True
    p.update()

    curr_ssid = wifi_helper.get_current_ssid()
    networks = wifi_helper.get_networks()

    for n in networks:
        ico = ft.Icon(ft.icons.DONE)
        btn = ft.TextButton(
            content=ft.Container(content=ft.Row(controls=[ico, ft.Text(n)])),
            on_click=lambda e, name=n: open_connection_dialog(name),
        )

        if (curr_ssid != n):
            ico.visible = False

        wifi_list.controls.append(btn)

    wifi_loading.value = ""
    p.update()


ico_wifi = ft.IconButton(icon=ft.icons.WIFI, icon_size=25, icon_color=ft.colors.BLACK,
                         on_click=lambda e: open_wifi_dialog())
ico_bluetooth = ft.Icon(name=ft.icons.BLUETOOTH, size=25)

volume_icon = ft.Icon(name=ft.icons.VOLUME_UP_ROUNDED, size=25, color=ft.colors.BLACK)
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


radio_search_listview = ft.ListView(spacing=10, padding=20, expand=True)

duplicate_text = ft.Text("")
duplicate_dialog = ft.AlertDialog(
    title=duplicate_text,
    actions=[
        ft.FilledButton("Ok", on_click=lambda e: close_duplicate_dialog())
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)


def close_duplicate_dialog():
    duplicate_dialog.open = False
    p.update()


def add_station(station):
    stations_list = stations_helper.load_radio_stations()
    found = False
    for el in stations_list:
        if el["name"] == station["name"]:
            found = True
            duplicate_text.value = f'{constants.current_station_to_add["name"]} existiert bereits'
            duplicate_dialog.open = True
            p.update()
            break

    if not found:
        stations_helper.add_station(station)
        reload_radio_stations(p)
        close_station_add_dialog()


station_to_add_text = ft.Text(f'{constants.current_station_to_add["name"]}')
station_add_dialog = ft.AlertDialog(
    content=ft.Column(
        width=500,
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER
    ),
    title=station_to_add_text,
    actions=[
        ft.FilledButton("Abspielen", on_click=lambda e: change_radio_station(constants.current_station_to_add, p)),
        ft.FilledButton("Zu Liste hinzufügen", on_click=lambda e: add_station(constants.current_station_to_add))
    ],
    actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
)


def close_station_add_dialog():
    station_add_dialog.open = False
    p.update()


def open_station_add_dialog(element, page: ft.Page):
    constants.current_station_to_add = element
    station_to_add_text.value = element["name"]
    station_add_dialog.update()
    station_add_dialog.open = True
    page.update()


def search_stations():
    name = radio_search_textfield.value
    stations = radio_helper.get_stations_by_name(name)
    l = []
    for el in stations:
        img = ft.Container(ft.Icon(ft.icons.MUSIC_NOTE), width=60, height=60) if el["logo"] == "" else ft.Image(
            el["logo"], fit=ft.ImageFit.SCALE_DOWN, border_radius=ft.border_radius.all(10), width=50, height=50)
        element = ft.Container(
            ft.Row([
                img,
                ft.Column([
                    ft.Text(el["name"], weight=ft.FontWeight.BOLD),
                    ft.Text(el["src"])
                ])
            ]),
            on_click=lambda e, item=el: open_station_add_dialog(item, p)
        )

        l.append(element)

    radio_search_listview.controls = l
    p.update()


radio_search_textfield = ft.TextField(
    label="Radiosender",
    expand=True,
    on_focus=lambda e: system_helper.open_keyboard(),
    on_blur=lambda e: system_helper.close_keyboard()
)

radio_search_dialog = ft.AlertDialog(
    content=ft.Column(
        width=600,
        expand=True,
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                [
                    radio_search_textfield,
                    ft.FilledButton("Suchen", on_click=lambda e: search_stations()),
                ],
                spacing=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            radio_search_listview
        ]
    )
)


def open_radio_search_dialog():
    radio_search_dialog.open = True
    p.update()


song_info_station = ft.Text("Kein Radiosender ausgewählt", weight=ft.FontWeight.BOLD)
song_info_title = ft.Text("", expand=True)
song_info_row = ft.Row([
    ft.Icon(ft.icons.MUSIC_NOTE),
    song_info_station,
    song_info_title,
    ft.TextButton("Sendersuche", icon=ft.icons.SEARCH, on_click=lambda e: open_radio_search_dialog())
])


def reset_song_info_row(page: ft.Page):
    constants.current_radio_station = {}
    song_info_station.value = "Kein Radiosender ausgewählt"
    song_info_title.value = ""
    p.update()


def update_song_info(page: ft.Page):
    try:
        title = radio_helper.get_song_info(constants.current_radio_station["src"])

        if title != "":
            song_info_station.value = constants.current_radio_station["name"]
            song_info_title.value = title
        else:
            song_info_station.value = constants.current_radio_station["name"]
            song_info_title.value = ""
    except:
        pass

    page.update()


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


def background_processes(page: ft.Page):
    while True:
        update_connected_device(page)
        update_taskbar(page)
        update_song_info(page)
        time.sleep(5)


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
        volume_icon.name = ft.icons.VOLUME_OFF_ROUNDED
        volume_icon.color = ft.colors.RED
        volume_text.value = ""
    else:
        volume_icon.name = ft.icons.VOLUME_UP_ROUNDED
        volume_icon.color = ft.colors.BLACK
        volume_text.value = f"{audio_helper.get_volume()}%"

    page.update()


def disable_indicator():
    for ref in constants.indicator_refs:
        ref.current.visible = False


def toggle_indicator(index):
    print(index)
    disable_indicator()
    if index != -1:
        constants.indicator_refs[index].current.visible = True


def change_radio_station(station, page, index=-1):
    global strip_color
    color = station["color"]

    station_add_dialog.open = False
    constants.current_radio_station = station

    toggle_indicator(index)
    page.theme.color_scheme_seed = color
    page.navigation_bar.bgcolor = color
    audio_helper.play_src(station["src"])
    strip.update_strip(color)

    update_song_info(page)

    page.update()


def start_rotary(page: ft.Page):
    rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
    rotary.setup(step=VOLUME_STEP,
                 inc_callback=lambda e: inc_sound(page), dec_callback=lambda e: dec_sound(page),
                 sw_callback=lambda: toggle_mute(page))
    rotary_thread = threading.Thread(target=rotary.watch)
    rotary_thread.start()


def main(page: ft.Page):
    global p, txt_discovery_status, ico_discovery_status, btn_discovery_status, txt_device_connected, ico_device_connected, btn_device_connected, ico_wifi, ico_bluetooth, volume_icon, volume_text, wifi_dialog, wifi_connection_dialog, radio_search_dialog, station_add_dialog, background_processes, radio_grid, duplicate_dialog, station_delete_dialog
    start_rotary(page)
    GpioButton(21, audio_helper.play_toast)

    page.window_maximized = True
    page.window_frameless = True
    page.spacing = 0
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
    page.add(radio_search_dialog)
    page.add(station_add_dialog)
    page.add(duplicate_dialog)
    page.add(station_delete_dialog)

    page.appbar = ft.AppBar(
        leading=ft.Row([
            volume_icon,
            volume_text
        ],
            spacing=10
        ),
        title=ft.Text("Retro.I"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        toolbar_height=40,
        actions=[ico_wifi, ico_bluetooth],
    )

    page.update()

    update_taskbar(page)

    def change_tab(e):
        tab_index = e.control.selected_index
        update_song_info(page)

        if tab_index == 0:
            switch_radio_tab()
            bluetooth_helper.turn_off()
            update_taskbar(page)
        else:
            radio_tab.visible = False
            reset_song_info_row(page)

        if tab_index == 1:
            switch_bluetooth_tab()
            disable_indicator()
            bluetooth_helper.turn_on()
            update_taskbar(page)
        else:
            bluetooth_tab.visible = False

        if system_helper.is_party_mode():
            if tab_index == 2:
                switch_soundboard_tab()
                disable_indicator()
            else:
                soundboard_tab.visible = False

            if tab_index == 3:
                settings_tab.visible = True
            else:
                settings_tab.visible = False
        else:
            if tab_index == 2:
                settings_tab.visible = True
            else:
                settings_tab.visible = False

        page.update()

    def switch_radio_tab():
        if bluetooth_helper.is_discovery_on():
            toggle_bluetooth_discovery(page)
        bluetooth_helper.disconnect()
        update_connected_device(page)
        radio_tab.visible = True

    def switch_bluetooth_tab():
        audio_helper.pause()
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

    page.navigation_bar = ft.NavigationBar(
        bgcolor="green",
        on_change=change_tab,
        selected_index=0,
        destinations=destinations
    )

    soundboard_grid = ft.GridView(
        expand=True,
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
                              expand=True)
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
    lv.controls.append(SettingsButton.get(ft.icons.LOGOUT, "Radio ausschalten", show_dialog))
    lv.controls.append(SettingsButton.get(ft.icons.COLOR_LENS, "LED-Streifen", show_led_dialog))
    lv.controls.append(SettingsButton.get(ft.icons.INFO, "Info", show_info_dialog))
    lv.controls.append(SettingsButton.get(ft.icons.STAR, "Credits", show_credits_dialog))

    reload_radio_stations(page)

    # Card for toast (drinking)
    soundboard_grid.controls.append(ToastCard.get(page))

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
            song_info_row,
            ft.Row([radio_grid])
        ]),
        margin=ft.margin.only(right=75)
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

    if system_helper.is_party_mode():
        tabs.append(soundboard_tab)

    tabs.append(settings_tab)

    page.add(ft.Column(tabs))
    page.update()

    p = page
    p.update()

    audio_helper.startup_sound()

    background_processes = threading.Thread(target=background_processes(page))
    background_processes.start()


ft.app(main)
