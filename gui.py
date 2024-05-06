import json



import flet as ft

from RadioStream import RadioStream


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
