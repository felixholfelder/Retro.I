import RPi.GPIO as GPIO
import json
import flet as ft
import threading
import subprocess
import time
from Audio import Audio
from Stations import Stations
from pyky040 import pyky040
from System import System
from multiprocessing import Process
from BluetoothHelper import BluetoothHelper
from Strip import Strip
from adafruit_led_animation.color import BLUE, GREEN

CLK_PIN = 26
DT_PIN = 17
SW_PIN = 16

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 3

last_turn = 1

bluetooth_helper = BluetoothHelper()
audio_helper = Audio()
system_helper = System()
stations_helper = Stations()
strip = Strip()
strip.start()

bluetooth_helper.bluetooth_discovery_off()
btn_discovery_status = None
btn_device_connected = None

def enable_discovery():
    bluetooth_helper.bluetooth_discovery_on()
    btn_discovery_status.text = "Bluetooth sichtbar"
    btn_discovery_status.icon = ft.icons.BLUETOOTH
    btn_discovery_status.style.bgcolor = ft.colors.GREEN


def disable_discovery():
    bluetooth_helper.bluetooth_discovery_off()
    btn_discovery_status.text = "Bluetooth nicht sichtbar"
    btn_discovery_status.icon = ft.icons.BLUETOOTH_DISABLED
    btn_discovery_status.style.bgcolor = ft.colors.RED


def toggle_bluetooth_discovery(page: ft.Page):
    discovery_on = bluetooth_helper.is_discovery_on()
    if discovery_on:
        disable_discovery()
    else:
        enable_discovery()
    page.update()


def get_connected_devices(page):
    result = subprocess.run(['bluetoothctl', 'devices', 'Connected'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if result != "":
        name = result[25:]
        mac = result[7:24]
        btn_device_connected.text = f"Verbunden mit: {name}"
        btn_device_connected.icon = ft.icons.PHONELINK
        disable_discovery()
    else:
        btn_device_connected.text = "Kein Gerät verbunden"
        btn_device_connected.icon = ft.icons.PHONELINK_OFF

    page.update()


def bluetooth_listener(page):
    while True:
        get_connected_devices(page)
        time.sleep(30)


def update_sound(value, page: ft.Page):
    if not audio_helper.is_mute():
        audio_helper.update_sound(value)
        # TODO - change slider for volume
        strip.update_sound_strip(value)
        page.update()

def inc_sound(value, page: ft.Page):
    global last_turn
    if last_turn == 1:
        update_sound(value, page)
    last_turn = 1


def dec_sound(value, page: ft.Page):
    global last_turn
    if last_turn == 0:
        update_sound(value, page)
    last_turn = 0


def toggle_mute(page: ft.Page):
    is_mute = audio_helper.toggle_mute()
    strip.toggle_mute(is_mute)
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

def toggle_indicator(station):
    disable_indicator()
    indicator_refs[station[0]].current.visible = True


def change_radio_station(event: ft.ContainerTapEvent, page):
    global strip_color
    station = get_station_by_image(event.control.image_src)
    color = station[1]["color"]

    toggle_indicator(station)
    page.theme = ft.Theme(color_scheme_seed=color)
    page.navigation_bar.bgcolor = color
    audio_helper.play(station[1]["src"])
    page.update()

    strip.run(color)


def start_rotary(page: ft.Page):
    # TODO - start rotary at current volume
    rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
    rotary.setup(scale_min=MIN_VOLUME, scale_max=MAX_VOLUME, step=VOLUME_STEP,
                 inc_callback=lambda e: inc_sound(e, page), dec_callback=lambda e: dec_sound(e, page),
                 sw_callback=lambda: toggle_mute(page))
    rotary_thread = threading.Thread(target=rotary.watch)
    rotary_thread.start()


def main(page: ft.Page):
    global btn_discovery_status, btn_device_connected
    start_rotary(page)
    # page.window_full_screen = True
    page.window_maximized = True
    page.theme = ft.Theme(color_scheme_seed='green')
    page.overlay.append(audio_helper.init())
    page.scroll = ft.ScrollMode.ALWAYS
    page.update()

    def change_tab(e):
        index = e.control.selected_index
        if index == 0:
            switch_radio_tab()
        else: radio_tab.visible = False

        if index == 1:
            switch_bluetooth_tab()
        else: bluetooth_tab.visible = False
    
        if index == 2:
            settings_tab.visible = True
        else: settings_tab.visible = False

        page.update()

    def switch_radio_tab():
        if bluetooth_helper.is_discovery_on():
            toggle_bluetooth_discovery(page)
        bluetooth_helper.disconnect()
        disable_indicator()
        strip.fill(GREEN)
        radio_tab.visible = True

    def switch_bluetooth_tab():
        audio_helper.pause()
        strip.fill(BLUE)
        bluetooth_tab.visible = True

    nav = ft.NavigationBar(
        bgcolor="green",
        on_change=change_tab,
        selected_index=0,
        destinations=[
            ft.NavigationDestination(
                label="Radiosender",
                icon=ft.icons.RADIO_OUTLINED,
                selected_icon=ft.icons.RADIO
            ),
            ft.NavigationDestination(
                label="Bluetooth",
                icon=ft.icons.BLUETOOTH,
                selected_icon=ft.icons.BLUETOOTH
            ),
            ft.NavigationDestination(
                label="Einstellungen",
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS
            )
        ]
    )
    page.navigation_bar = nav

    grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=50,
        visible=True,
    )

    radio_stations = ft.Column(
        [grid],
    )

    radio_tab = ft.Container(
        radio_stations,
        expand=True,
    )

    dlg = ft.AlertDialog(
        content=ft.Column(
            controls=[
                ft.TextButton("Radio ausschalten", on_click=system_helper.shutdown_system, icon=ft.icons.POWER_OFF),
                ft.TextButton("Radio neustarten", on_click=system_helper.restart_system, icon=ft.icons.REPLAY)
            ]
        )
    )
    page.add(dlg)

    def show_dialog(_):
        dlg.open = True
        page.update()

    lv = ft.ListView(expand=1, spacing=10, padding=20)
    lv.controls.append(ft.TextButton("Radio ausschalten", on_click=show_dialog, icon=ft.icons.LOGOUT))
    settings_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Einstellungen", size=24),
                lv
            ]
        ),
        visible=False,
    )

    for index, i in enumerate(stations_helper.load_radio_stations()):
        indicator_refs.append(ft.Ref[ft.Image]())
        grid.controls.append(
            ft.Stack(
                alignment=ft.MainAxisAlignment.END,
                fit=ft.StackFit.EXPAND,
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.GREEN_50,
                        on_click=lambda e: change_radio_station(e, page),
                        border_radius=10,
                        image_src=system_helper.get_img_path(i["logo"]),
                    ),
                    ft.Image(ref=indicator_refs[index], src=f"{system_helper.pwd()}/assets/party.gif", opacity=0.7,
                             visible=False)
                ]
            )
        )

    btn_discovery_status = ft.FilledButton(
        "Bluetooth nicht sichtbar",
        icon=ft.icons.BLUETOOTH_DISABLED,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED,
        ),
        width=300,
        on_click=lambda e: toggle_bluetooth_discovery(page),
    )
    
    btn_device_connected = ft.TextButton(
        "Verbunden mit: A34 von Felix",
        icon=ft.icons.PHONELINK_OFF,
        width=300,
        on_click=lambda e: get_connected_devices(page),
    )

    bluetooth_tab = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                btn_discovery_status,
                btn_device_connected
            ]
        ),
        visible=False,
    )

    page.add(
        ft.Column(
            [radio_tab, bluetooth_tab, settings_tab],
            expand=True,
        )
    )
    page.update()
    
    bluetooth_process = Process(target=bluetooth_listener(page))
    bluetooth_process.start()

ft.app(main)
