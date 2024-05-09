import RPi.GPIO as GPIO
import json
import flet as ft
import threading
from Audio import Audio
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

def update_sound(value, page: ft.Page):
    audio_helper.update_sound(value)
    # TODO - change slider for volume
    # TODO - change color of led-stripe
    page.update()


def toggle_mute(page: ft.Page):
    audio_helper.toggle_mute()
    page.update()
    # TODO - change color of led-stripe


# TODO - move this function to file and create list with objects
def load_radio_stations():
    f = open('radio-stations.json')
    data = json.load(f)
    f.close()
    return data


def get_station_by_image(src):
    for i, obj in enumerate(load_radio_stations()):
        if f"./assets/stations/{obj['logo']}" == src:
            return obj
    return -1

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


audio = ft.Audio(
    src=load_radio_stations()[0]["url"], autoplay=False
)


def change_radio_station(event: ft.ContainerTapEvent, page):
    station = get_station_by_image(event.control.image_src)
    print(station)
    audio.pause()
    audio.src = station["url"]
    audio.play()
    audio.update()


def start_rotary(page: ft.Page):
    # TODO - start rotary at current volume
    rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
    rotary.setup(scale_min=MIN_VOLUME, scale_max=MAX_VOLUME, step=VOLUME_STEP, inc_callback=lambda e: update_sound(e, page), dec_callback=lambda e: update_sound(e, page), sw_callback=lambda: toggle_mute(page))
    rotary_thread = threading.Thread(target=rotary.watch)
    rotary_thread.start()


def main(page: ft.Page):
    start_rotary(page)

    page.theme = ft.Theme(color_scheme_seed='green')
    page.overlay.append(audio)
    page.window_maximized = True
    # page.window_full_screen = True
    page.scroll = ft.ScrollMode.ALWAYS  # TODO - fix infinity scroll
    page.update()
    load_radio_stations()

    def change_tab(e):
        index = e.control.selected_index
        radio_tab.visible = True if index == 0 else False
        settings_tab.visible = True if index == 1 else False
        page.update()

    page.navigation_bar = ft.NavigationBar(
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

    radio_tab = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=50,
        visible=True
    )

    dlg = ft.AlertDialog(
        content=ft.Column(
            controls=[
                ft.TextButton(f"Radio ausschalten", on_click=system_helper.shutdown_system, icon=ft.icons.POWER_OFF,
                              style=ft.ButtonStyle(color=ft.colors.WHITE)),
                ft.TextButton(f"Radio neustarten", on_click=system_helper.restart_system, icon=ft.icons.REPLAY,
                              style=ft.ButtonStyle(color=ft.colors.WHITE))
            ]
        )
    )
    page.dialog = dlg

    def show_dialog(_):
        dlg.open = True
        page.update()

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lv.controls.append(ft.TextButton(f"Radio ausschalten", on_click=show_dialog, icon=ft.icons.LOGOUT,
                                     style=ft.ButtonStyle(color=ft.colors.WHITE)))
    settings_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Einstellungen", size=24),
                lv
            ]
        ),
        visible=False,
    )

    for i in load_radio_stations():
        radio_tab.controls.append(
            ft.Container(
                bgcolor=ft.colors.GREEN_50,
                on_click=lambda e: change_radio_station(e, page),
                border_radius=10,
                image_src=f"./assets/stations/{i['logo']}",
            )
        )

    page.add(
        ft.Container(
            content=ft.Column([
                radio_tab,
                settings_tab
            ])
        )
    )
    page.update()


ft.app(main)