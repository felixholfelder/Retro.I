import RPi.GPIO as GPIO
import time
import json
import flet as ft
from RadioStream import RadioStream
import threading
from Audio import Audio
from pyky040 import pyky040

LED_PIN = 8

CLK_PIN = 21
DT_PIN = 16
SW_PIN = 15

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 5

audio = Audio()

def update_sound(value):
    audio.update_sound(value)


def toggle_mute():
    mute = audio.toggle_mute()
    GPIO.output(LED_PIN, mute)

rotary = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
rotary.setup(scale_min=MIN_VOLUME, scale_max=MAX_VOLUME, step=VOLUME_STEP, loop=True, inc_callback=update_sound, dec_callback=update_sound, sw_callback=toggle_mute)

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


def get_current_volume():
    return audio.mixer().getvolume[0]


def update_sound(value):
    audio.Mixer().setvolume(int(value))
    prev_volume = int(value)
    #TODO - show sound slider


def load_radio_stations():
    f = open('radio-stations.json')
    data = json.load(f)
    f.close()
    return data


def get_index_by_image(src):
    for i, obj in enumerate(load_radio_stations()):
        if f"./assets/stations/{obj['logo']}" == src:
            return obj
    return -1

my_thread = threading.Thread(target=rotary.watch)
my_thread.start()

#slider = ft.Slider(min=MIN_VOLUME, max=MAX_VOLUME, divisions=20, label="{value}%", value=get_current_volume(), on_change=lambda event: update_sound(event.control.value))


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed='green')
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
            ft.NavigationDestination(label="Radiosender", icon=ft.icons.RADIO),
            ft.NavigationDestination(label="Einsellungen", icon=ft.icons.SETTINGS)
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
    settings_tab = ft.Text("Tab 2", size=30, visible=False)

    page.add(radio_tab)

    def switch_radio_station(event):
        obj = get_index_by_image(event.control.content.src)
        stream = RadioStream()
        stream.stream(obj["url"])

    for i in load_radio_stations():
        radio_tab.controls.append(
            ft.Card(
                content=ft.Container(
                    on_click=switch_radio_station,
                    border_radius=10,
                    content=ft.Image(
                        src=f"./assets/stations/{i['logo']}",
                        fit=ft.ImageFit.FIT_WIDTH,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ))
            )
        )
    page.update()

    page.add(
        ft.Container(
            content=ft.Column([
                radio_tab,
                settings_tab
            ])
        )
    )


ft.app(main)
