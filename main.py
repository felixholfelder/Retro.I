import RPi.GPIO as GPIO
import json
import flet as ft
import threading
from Audio import Audio
from Stations import Stations
from pyky040 import pyky040
from System import System
from multiprocessing import Process
from Strip import Strip

CLK_PIN = 26
DT_PIN = 4
SW_PIN = 21

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 1

volume_updates = 0

audio_helper = Audio()
system_helper = System()
stations_helper = Stations()
strip = Strip()
strip.start()


def get_path(img_src):
    return f"{system_helper.pwd()}/assets/stations/{img_src}"


def update_sound(value, page: ft.Page):
    global volume_updates
    if not audio_helper.is_mute():
        if (volume_updates % 2 == 0):
            audio_helper.update_sound(value)
            # TODO - change slider for volume
            strip.update_sound_strip(value)
            page.update()
        volume_updates += 1


def toggle_mute(page: ft.Page):
    is_mute = audio_helper.toggle_mute()
    strip.toggle_mute(is_mute)
    page.update()


def get_station_by_image(src):
    for i, obj in enumerate(stations_helper.load_radio_stations()):
        if get_path(obj["logo"]) == src:
            return [i, obj]
    return -1


indicator_refs = []

def toggle_indicator(station):
    for ref in indicator_refs:
        ref.current.visible = False

    indicator_refs[station[0]].current.visible = True

def update_strip():
    while True:
        blink.animate()

def change_radio_station(event: ft.ContainerTapEvent, page):    
    global strip_color
    station = get_station_by_image(event.control.image_src)
    color = station[1]["color"]

    toggle_indicator(station)
    page.theme = ft.Theme(color_scheme_seed=color)
    page.navigation_bar.bgcolor = color
    #audio_helper.play(station[1]["src"])
    page.update()
    
    strip.run(color)


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
    #page.window_full_screen = True
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
                        image_src=get_path(i["logo"]),
                    ),
                    ft.Image(ref=indicator_refs[index], src=f"{system_helper.pwd()}/assets/party.gif", opacity=0.7, visible=False)
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

#main_proc = Process(target=ft.app(main))
#main_proc.start()
ft.app(main)
