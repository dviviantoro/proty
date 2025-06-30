import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.template_ui import grid_database
from modules.database import tinydb_insert_dict, tinydb_check_existence, tinydb_read
from pages.theme import frame
from modules.util import *

def load_database(grid):
    tables = ["background", "calibration", "acquisition"]
    rows = []
    for i in tables:
        for data in tinydb_read(i):
            filtered_data = {key: data[key] for key in keys_database}
            filtered_data["category"] = i
            rows.append(filtered_data)
    grid.options["rowData"] = rows
    grid.update()

def page() -> None:
    with frame("Background Sampling Panel", 'You have to turn on all services'):
        with ui.element('div').classes('absolute-center'):
            with ui.row().classes("w-full place-content-center"):
                grid = ui.aggrid(grid_database()).classes('h-[340px] w-[840px]')
                load_database(grid)
            with ui.row().classes("w-full place-content-center"):
                with ui.button_group():
                    ui.button(
                    "Delete",
                    icon="delete",
                    color="red",
                )
                    ui.button(
                    "View",
                    icon="pageview",
                    color="blue",
                )