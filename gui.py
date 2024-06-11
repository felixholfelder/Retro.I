import flet as ft
from bluetooth import *
from pybtooth import BluetoothManager

from BluetoothHelper import BluetoothHelper
from Stations import Stations
# from pyky040 import pyky040
from System import System

CLK_PIN = 26
DT_PIN = 17
SW_PIN = 16

MIN_VOLUME = 0
MAX_VOLUME = 100
VOLUME_STEP = 3

last_turn = 1

system_helper = System()
stations_helper = Stations()
bluetooth_helper = BluetoothHelper()

btn_discovery_status = None


def toggle_bluetooth_discovery(_, page: ft.Page):
    discovery_on = bluetooth_helper.toggle_bluetooth_discovery(page)
    if discovery_on:
        btn_discovery_status.text = "Bluetooth sichtbar"
        btn_discovery_status.icon = ft.icons.BLUETOOTH
        btn_discovery_status.style.bgcolor = ft.colors.GREEN
    else:
        btn_discovery_status.text = "Bluetooth nicht sichtbar"
        btn_discovery_status.icon = ft.icons.BLUETOOTH_DISABLED
        btn_discovery_status.style.bgcolor = ft.colors.RED
    page.update()
    bm = BluetoothManager()
    connected = bm.getConnectedDevices()
    print(connected)


def update_sound(value, page: ft.Page):
    pass


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
    pass


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


def change_radio_station(event: ft.ContainerTapEvent, page):
    global strip_color
    station = get_station_by_image(event.control.image_src)
    color = station[1]["color"]

    toggle_indicator(station)
    page.theme = ft.Theme(color_scheme_seed=color)
    page.navigation_bar.bgcolor = color
    # audio_helper.play(station[1]["src"])
    page.update()

    # strip.run(color)


def start_rotary(page: ft.Page):
    pass


def main(page: ft.Page):
    global btn_discovery_status
    start_rotary(page)
    # page.window_full_screen = True
    page.window_maximized = True
    page.theme = ft.Theme(color_scheme_seed='green')
    # page.overlay.append(audio_helper.init())
    page.scroll = ft.ScrollMode.ALWAYS
    page.update()

    def change_tab(e):
        index = e.control.selected_index
        radio_tab.visible = True if index == 0 else False
        bluetooth_tab.visible = True if index == 1 else False
        settings_tab.visible = True if index == 2 else False
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
                        image_src=get_path(i["logo"]),
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
        on_click=lambda e: toggle_bluetooth_discovery(e, page),
    )

    bluetooth_tab = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                btn_discovery_status
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

ft.app(main)
