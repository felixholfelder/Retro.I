import flet as ft


def main(page: ft.Page):
    page.update()

    def changetab(e):
        index = e.control.selected_index
        tab_1.visible = True if index == 0 else False
        tab_2.visible = True if index == 1 else False
        page.update()

    page.navigation_bar = ft.NavigationBar(
        bgcolor="blue",
        on_change=changetab,
        selected_index=0,
        destinations=[
            ft.NavigationDestination(label="Radiosender", icon=ft.icons.RADIO),
            ft.NavigationDestination(label="Einsellungen", icon=ft.icons.SETTINGS)
        ]
    )

    tab_1 = ft.Text("Tab 1", size=30, visible=True)
    tab_2 = ft.Text("Tab 2", size=30, visible=False)

    page.add(
        ft.Container(
            content=ft.Column([
                tab_1,
                tab_2
            ])
        )
    )


ft.app(main)
