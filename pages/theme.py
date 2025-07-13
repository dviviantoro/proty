import os, sys
from contextlib import contextmanager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

ui.button.default_props('no-caps')
ui.add_css("""
    .q-btn {
        box-shadow: none !important;
    }
""")

def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to('/login')

@contextmanager
def frame(my_head: str, my_foot: str):
    with ui.column().classes('absolute-center items-center h-screen no-wrap p-9 w-full'):
        yield
    
    with ui.header().classes(replace='row items-center').style('display: flex; justify-content: space-between; width: 100%; background-color: #3874c8'):
        with ui.row().classes('items-center'):
            with ui.button(on_click=lambda:ui.navigate.back(), color="clear").props("flat"):
                ui.image(logo_img).classes('rounded-full w-10 h-10')

            ui.label(my_head)
        with ui.button(icon='menu').props('flat color=white'):
            with ui.menu() as menu:
                ui.menu_item('Menu item 1', on_click=lambda:ui.navigate.to("/scope"))
                ui.separator()
                ui.menu_item('Close', menu.close)
                ui.menu_item('Logout', logout)
         
    with ui.footer().style('background-color: #3874c8'):
        with ui.row().style('display: flex; justify-content: space-between; width: 100%;'):
            ui.label(my_foot)
            ui.label("v25.2")