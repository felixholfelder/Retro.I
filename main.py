import threading
import time

from helper.dialogs.StationDeleteDialog import StationDeleteDialog

from components.BluetoothDeviceConnected import BluetoothDeviceConnected
from components.BluetoothDiscoveryToggle import BluetoothDiscoveryToggle
from components.NavigationBar import NavigationBar
from components.Rotary import Rotary
from components.SongInfoRow import SongInfoRow
from components.Taskbar import Taskbar
from components.dialogs.DuplicateDialog import DuplicateDialog
from components.dialogs.SettingsCreditsDialog import SettingsCreditsDialog
from components.dialogs.SettingsInfoDialog import SettingsInfoDialog
from components.dialogs.SettingsLedDialog import SettingsLedDialog
from components.dialogs.SettingsShutdownDialog import SettingsShutdownDialog
from components.dialogs.StationAddDialog import StationAddDialog
from components.view.Theme import Theme
from scripts import button
import flet as ft
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

p = None

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

theme = Theme()

bluetooth_helper.turn_on()
bluetooth_helper.bluetooth_discovery_off()
bluetooth_helper.turn_off()

radio_grid = ft.GridView(
    expand=True,
    runs_count=5,
    max_extent=150,
    child_aspect_ratio=1.0,
    spacing=20,
    run_spacing=50
)


def open_delete_station_dialog(index):
    constants.current_station_index_to_delete = index
    station_delete_dialog.open()


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
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREY_200,
                        on_click=lambda e, src=station, p=page, index=i: change_radio_station(src, p, index),
                        on_long_press=lambda e, index=i: open_delete_station_dialog(index),
                        border_radius=10,
                        # TODO - expand???
                        content=ft.Image(src=system_helper.get_img_path(station["logo"]),
                                         border_radius=ft.border_radius.all(4), fit=ft.ImageFit.FIT_WIDTH) if station[
                                                                                                                  "logo"] != "" else ft.Text(
                            station["name"], text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
                        padding=10,
                    ),
                    ft.Image(ref=constants.indicator_refs[i], src=f"{constants.pwd()}/assets/party.gif", opacity=0.7,
                             visible=False)
                ]
            )
        )

    if page is not None:
        page.update()


def delete_dialog():
    stations_helper.delete_station(constants.current_station_index_to_delete)
    reload_radio_stations(p)


station_delete_dialog = StationDeleteDialog(delete_dialog)

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
    taskbar.update()
    p.update()

    wifi_helper.connect_to_wifi(ssid, wifi_connection_dialog_pass.value)

    wifi_connection_dialog_pass.value = ""

    close_connection_dialog()
    wifi_connection_dialog_btn.disabled = False
    wifi_connection_dialog_btn.text = "Verbinden"
    taskbar.update()
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


taskbar = Taskbar(open_wifi_dialog)

btn_discovery_status = BluetoothDiscoveryToggle()
btn_device_connected = BluetoothDeviceConnected(taskbar, btn_discovery_status.disable_discovery())

radio_search_listview = ft.ListView(spacing=10, padding=20, expand=True)
duplicate_dialog = DuplicateDialog()


def add_station(station):
    stations_list = stations_helper.load_radio_stations()
    found = False
    for el in stations_list:
        if el["name"] == station["name"]:
            found = True
            duplicate_dialog.open(constants.current_station_to_add["name"])
            break

    if not found:
        stations_helper.add_station(station)
        reload_radio_stations(p)

def disable_indicator():
    for ref in constants.indicator_refs:
        ref.current.visible = False


def toggle_indicator(index):
    disable_indicator()
    if index != -1:
        constants.indicator_refs[index].current.visible = True


def change_radio_station(station, page, index=-1):
    global strip_color
    color = station["color"]

    constants.current_radio_station = station

    toggle_indicator(index)
    theme.update(color)
    page.navigation_bar.bgcolor = color
    audio_helper.play_src(station["src"])
    strip.update_strip(color)

    song_info_row.update()

    page.update()

station_add_dialog = StationAddDialog(change_radio_station(constants.current_station_to_add, p), add_station)

radio_not_found_text = ft.Text("Kein Radiosender gefunden!", visible=False)


def search_stations():
    name = radio_search_textfield.value
    stations = radio_helper.get_stations_by_name(name)

    if len(stations) == 0:
        radio_not_found_text.visible = True
    else:
        radio_not_found_text.visible = False

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
            on_click=lambda e, item=el: station_add_dialog.open(item)
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
            radio_not_found_text,
            radio_search_listview
        ]
    )
)


def open_radio_search_dialog():
    radio_search_dialog.open = True
    p.update()


song_info_row = SongInfoRow(open_radio_search_dialog)


def background_processes():
    while True:
        btn_device_connected.update_connected_device(btn_discovery_status.disable_discovery())
        taskbar.update()
        song_info_row.update()
        time.sleep(5)


def main(page: ft.Page):
    global p, wifi_dialog, wifi_connection_dialog, radio_search_dialog, station_add_dialog, background_processes, radio_grid, duplicate_dialog, station_delete_dialog, song_info_row, theme
    GpioButton(21, audio_helper.play_toast)

    page.window_maximized = True
    page.window_frameless = True
    page.spacing = 0
    page.theme = theme.get()
    page.add(audio_helper.init())
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.title = "Retro.I"

    page.add(wifi_dialog)
    page.add(wifi_connection_dialog)
    page.add(radio_search_dialog)
    page.add(station_add_dialog.get())
    page.add(duplicate_dialog.get())
    page.add(station_delete_dialog.get())

    page.appbar = taskbar.get()
    taskbar.update()

    Rotary(taskbar, strip)

    def change_tab(e):
        tab_index = e.control.selected_index
        song_info_row.update()

        if tab_index == 0:
            switch_radio_tab()
            bluetooth_helper.turn_off()
            taskbar.update()
        else:
            radio_tab.visible = False
            song_info_row.reset()

        if tab_index == 1:
            switch_bluetooth_tab()
            disable_indicator()
            bluetooth_helper.turn_on()
            taskbar.update()
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
            btn_discovery_status.toggle_bluetooth_discovery()
        bluetooth_helper.disconnect()
        btn_device_connected.reset_connected_device()
        radio_tab.visible = True

    def switch_bluetooth_tab():
        audio_helper.pause()
        btn_device_connected.reset_connected_device()
        bluetooth_tab.visible = True

    def switch_soundboard_tab():
        soundboard_tab.visible = True

    page.navigation_bar = NavigationBar(change_tab).get()

    soundboard_grid = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=150,
        spacing=80,
        run_spacing=50
    )

    shutdown_dialog = SettingsShutdownDialog()
    led_dialog = SettingsLedDialog()
    info_dialog = SettingsInfoDialog()
    credits_dialog = SettingsCreditsDialog()

    page.add(shutdown_dialog.get())
    page.add(led_dialog.get())
    page.add(info_dialog)
    page.add(credits_dialog.get())

    lv = ft.ListView(spacing=10, padding=20)
    lv.controls.append(SettingsButton.get(ft.icons.LOGOUT, "Radio ausschalten", shutdown_dialog.open()))
    lv.controls.append(SettingsButton.get(ft.icons.COLOR_LENS, "LED-Streifen", led_dialog.open()))
    lv.controls.append(SettingsButton.get(ft.icons.INFO, "Info", info_dialog.open()))
    lv.controls.append(SettingsButton.get(ft.icons.STAR, "Credits", credits_dialog.open()))

    # Card for toast (drinking)
    soundboard_grid.controls.append(ToastCard.get(page))

    for i in range(len(sounds.load_sounds())):
        sound = sounds.load_sounds()[i]
        soundboard_grid.controls.append(SoundCard.get(page, sound["src"], sound["name"], i))

    # Tabs
    radio_tab = ft.Container(
        content=ft.Column([
            song_info_row.get(),
            ft.Row([radio_grid])
        ]),
        margin=ft.margin.only(right=75)
    )

    bluetooth_tab = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            spacing=50,
            controls=[
                btn_discovery_status.get(),
                btn_device_connected.get()
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

    reload_radio_stations(page)

    audio_helper.startup_sound()

    process = threading.Thread(target=background_processes())
    process.start()


ft.app(main)
