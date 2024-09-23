# import RPi.GPIO as GPIO
import json
import flet as ft
import threading
import time
from Audio import Audio
from Stations import Stations
# from pyky040 import pyky040
from System import System
from multiprocessing import Process
from BluetoothHelper import BluetoothHelper
from Strip import Strip
from Constants import Constants
from Sounds import Sounds
# from adafruit_led_animation.color import BLUE, GREEN

CLK_PIN = 26
DT_PIN = 17
SW_PIN = 16

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 2

last_turn = 1

bluetooth_helper = BluetoothHelper()
audio_helper = Audio()
system_helper = System()
stations_helper = Stations()
c = Constants()
sounds = Sounds()
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


def update_connected_device(page):
    name = bluetooth_helper.get_device_name()
    if name != "":
        btn_device_connected.text = f"Verbunden mit: {name}"
        btn_device_connected.icon = ft.icons.PHONELINK
        disable_discovery()
    else:
        btn_device_connected.text = "Kein Gerät verbunden"
        btn_device_connected.icon = ft.icons.PHONELINK_OFF

    page.update()


def bluetooth_listener(page):
    while True:
        update_connected_device(page)
        time.sleep(10)


def update_sound(value, page: ft.Page):
    if not audio_helper.is_mute():
        audio_helper.update_sound(value)
        strip.update_sound_strip(value)
        page.update()

def inc_sound(page: ft.Page):
    global last_turn
    if last_turn == 1:
        value = audio_helper.get_volume() + VOLUME_STEP
        update_sound(value, page)
    last_turn = 1


def dec_sound(page: ft.Page):
    global last_turn
    if last_turn == 0:
        value = audio_helper.get_volume() - VOLUME_STEP
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


def start_rotary(page: ft.Page):
    pass
    # rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
    # rotary.setup(scale_min=MIN_VOLUME, scale_max=MAX_VOLUME, step=VOLUME_STEP,
    #              inc_callback=lambda e: inc_sound(page), dec_callback=lambda e: dec_sound(page),
    #              sw_callback=lambda: toggle_mute(page))
    # rotary_thread = threading.Thread(target=rotary.watch)
    # rotary_thread.start()


def main(page: ft.Page):
    global btn_discovery_status, btn_device_connected
    start_rotary(page)
    #page.window_full_screen = True
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
            disable_indicator()
        else: bluetooth_tab.visible = False

        if index == 2:
            switch_soundboard_tab()
            disable_indicator()
        else: soundboard_tab.visible = False

        if index == 3:
            settings_tab.visible = True
        else: settings_tab.visible = False

        page.update()

    def switch_radio_tab():
        if bluetooth_helper.is_discovery_on():
            toggle_bluetooth_discovery(page)
        bluetooth_helper.disconnect()
        # strip.fill(GREEN)
        update_connected_device(page)
        radio_tab.visible = True

    def switch_bluetooth_tab():
        audio_helper.pause()
        #strip.fill(BLUE)
        update_connected_device(page)
        bluetooth_tab.visible = True

    def switch_soundboard_tab():
        audio_helper.pause()
        soundboard_tab.visible = True

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
                label="Soundboard",
                icon=ft.icons.SPACE_DASHBOARD_OUTLINED,
                selected_icon=ft.icons.SPACE_DASHBOARD
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
        run_spacing=50
    )

    soundboard_grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=50
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


    dlg_led = ft.AlertDialog(
        content=ft.Column(
            controls=[
                ft.Switch("LED-Streifen ausschalten", on_change=strip.toggle_strip, value=strip.is_strip_active())
            ]
        )
    )
    page.add(dlg_led)


    def show_dialog(_):
        dlg.open = True
        page.update()

    def show_led_dialog(_):
        dlg_led.open = True
        page.update()

    lv = ft.ListView(expand=1, spacing=10, padding=20)
    lv.controls.append(ft.TextButton("Radio ausschalten", on_click=show_dialog, icon=ft.icons.LOGOUT))
    lv.controls.append(ft.TextButton("LED-Streifen", on_click=show_led_dialog, icon=ft.icons.COLOR_LENS))
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
                    ft.Image(ref=indicator_refs[index], src=f"{c.pwd()}/assets/party.gif", opacity=0.7,
                             visible=False)
                ]
            )
        )

    for index, i in enumerate(sounds.load_sounds()):
        soundboard_grid.controls.append(
            ft.Container(
                alignment=ft.alignment.center,
                padding=10,
                bgcolor=ft.colors.GREEN_50,
                on_click=lambda e: audio_helper.play_sound(i["src"]),
                border_radius=10,
                content=ft.Text(i["name"], size=18),
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
        "Kein Gerät verbunden",
        icon=ft.icons.PHONELINK_OFF,
        width=300,
        on_click=lambda e: update_connected_device(page),
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

    soundboard_tab = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                soundboard_grid
            ]
        ),
        visible=False,
    )

    page.add(
        ft.Column(
            [radio_tab, bluetooth_tab, soundboard_tab, settings_tab],
            expand=True,
        )
    )
    page.update()

    bluetooth_process = Process(target=bluetooth_listener(page))
    bluetooth_process.start()

ft.app(main)
