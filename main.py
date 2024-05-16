import RPi.GPIO as GPIO
import json
import flet as ft
import threading
from Audio import Audio
from Stations import Stations
from pyky040 import pyky040
from System import System

LED_PIN = 14

CLK_PIN = 26
DT_PIN = 4
SW_PIN = 21

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 2

audio_helper = Audio()
system_helper = System()
stations_helper = Stations()


def get_path(img_src):
    return f"./assets/stations/{img_src}"


def update_sound(value, page: ft.Page):
    audio_helper.update_sound(value)
    # TODO - change slider for volume
    # TODO - change color of led-stripe
    page.update()


def toggle_mute(page: ft.Page):
    audio_helper.toggle_mute()
    page.update()
    # TODO - change color of led-stripe


def get_station_by_image(src):
    for i, obj in enumerate(stations_helper.load_radio_stations()):
        if get_path(obj["logo"]) == src:
            return [i, obj]
    return -1


GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

indicator_refs = []


def toggle_indicator(station):
    for ref in indicator_refs:
        ref.current.visible = False

    indicator_refs[station[0]].current.visible = True


def change_radio_station(event: ft.ContainerTapEvent, page):
    station = get_station_by_image(event.control.image_src)
    toggle_indicator(station)
    page.theme = ft.Theme(color_scheme_seed=station[1]["color"])
    page.navigation_bar.bgcolor = station[1]["color"]
    audio_helper.play(station[1]["src"])
    page.update()


def start_rotary(page: ft.Page):
    # TODO - start rotary at current volume
    rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
    rotary.setup(scale_min=MIN_VOLUME, scale_max=MAX_VOLUME, step=VOLUME_STEP,
                 inc_callback=lambda e: update_sound(e, page), dec_callback=lambda e: update_sound(e, page),
                 sw_callback=lambda: toggle_mute(page))
    rotary_thread = threading.Thread(target=rotary.watch)
    rotary_thread.start()


def main(page: ft.Page):
    start_rotary(page)

    # page.window_full_screen = True
    page.window_maximized = True
    page.theme = ft.Theme(color_scheme_seed='green')
    page.overlay.append(audio_helper.init())
    page.update()

    def change_tab(e):
        index = e.control.selected_index
        radio_tab.visible = True if index == 0 else False
        settings_tab.visible = True if index == 1 else False
        page.update()

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
        scroll=ft.ScrollMode.ALWAYS, # TODO - fix infinite scroll
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
    page.dialog = dlg

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
                        image_src=get_path(i["logo"]),
                    ),
                    ft.Image(ref=indicator_refs[index], src="./assets/party.gif", opacity=0.7, visible=False)
                ]
            )
        )

    page.add(
        ft.Column(
            [radio_tab, settings_tab],
            expand=True,
        )
    )
    page.update()


ft.app(main)
