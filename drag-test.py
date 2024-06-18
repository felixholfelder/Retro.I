import flet as ft

def main(page: ft.Page):
    # Create a scrollable container with a Column containing multiple Text widgets
    content = ft.Column(
        controls=[
            ft.Text(f"Item {i}") for i in range(1, 101)
        ],
        scroll="auto",
        expand=True
    )

    # Variables to store initial pointer position and scroll offset
    start_y = None
    scroll_y = None

    def on_pointer_down(e):
        nonlocal start_y, scroll_y
        start_y = e.y
        scroll_y = content.scroll_y

    def on_pointer_move(e):
        nonlocal start_y, scroll_y
        if start_y is not None:
            # Calculate new scroll position based on the movement
            offset = e.y - start_y
            new_scroll_y = scroll_y - offset
            # Update the scroll position
            content.scroll_to(new_scroll_y)

    def on_pointer_up(e):
        nonlocal start_y
        start_y = None

    # Attach pointer event handlers
    content.on_pointer_down = on_pointer_down
    content.on_pointer_move = on_pointer_move
    content.on_pointer_up = on_pointer_up

    # Add the scrollable container to the page
    page.add(content)
    page.update()

ft.app(target=main)
