import flet as ft
from flet_core import DismissDirection

counter = 0

def main(page):
    global counter
    page.snack_bar = ft.SnackBar(
        content=ft.Text(f"Hello {counter}"),
        dismiss_direction=DismissDirection.HORIZONTAL
    )
    page.snack_bar.open = True
    page.update()

    def on_click(e):
        global counter
        counter += 1
        page.snack_bar.content.update()
        page.update()
        print(counter)

    page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))

ft.app(target=main)