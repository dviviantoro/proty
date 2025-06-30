import os, sys
from nicegui import ui, app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.template_ui import generate_main_button, slide_phase_reset, slide_phase_swiped
from modules.database import tinydb_update_temp
from modules.util import *

@ui.page('/')
def content() -> None:
    tinydb_update_temp("phase", False)
    with ui.page_sticky(x_offset=18, y_offset=18, position="top"):
        with ui.list().props('bordered'):
            with ui.slide_item() as slide_item:
                with ui.item():
                    with ui.item_section().props('avatar'):
                        ui.icon('scatter_plot')
                    with ui.item_section():
                        ui.item_label('Phase Selection')
                        ui.item_label('swipe me to change phase').props('caption')
                with slide_item.left(color="#FFF085", on_slide=lambda: slide_phase_swiped("1 phase selected", 1)):
                    with ui.item(on_click= lambda:slide_phase_reset(slide_item)):
                        with ui.item_section().props('avatar'):
                            ui.icon('filter_1')
                        with ui.item_section():
                            ui.item_label('One phase')
                            ui.item_label('tap to reset').props('caption')
                with slide_item.right(color="#DA6C6C", on_slide=lambda: slide_phase_swiped("3 phase selected", 3)):
                    with ui.item(on_click= lambda:slide_phase_reset(slide_item)):
                        with ui.item_section():
                            ui.item_label('Three phase')
                            ui.item_label('tap to reset').props('caption')
                        with ui.item_section().props('avatar'):
                            ui.icon('filter_3')

    with ui.element('div').classes('grid grid-cols-12 absolute-center w-full gap-5'):
        with ui.card().style("border: none; background-color: transparent;").classes('no-shadow col-start-1 col-span-6 h-52'):
            with ui.element('div').classes('grid grid-cols-11 absolute-center w-full gap-5'):
                background = generate_main_button(
                    size="col-start-2 col-span-5",
                    title="Background Noise",
                    icon="blur_circular",
                    desc="Add or remove both sensor and background calibration preset",
                    to_address="/background"
                )

                calibration = generate_main_button(
                    size="col-start-7 col-span-5",
                    title="Sensor Calibration",
                    icon="all_out",
                    desc="Add or remove both sensor and background calibration preset",
                    to_address="/calibration"
                )

        with ui.card().style("border: none; background-color: transparent;").classes('no-shadow col-start-7 col-span-6 h-52'):
            with ui.element('div').classes('grid grid-cols-11 absolute-center w-full gap-5'):

                acquisition = generate_main_button(
                    size="col-start-1 col-span-5",
                    title="Start Acquisition",
                    icon="query_stats",
                    desc="Add or remove both sensor and background calibration preset",
                    to_address="/acquisition"
                )

                database = generate_main_button(
                    size="col-start-6 col-span-5",
                    title="Show Database",
                    icon="folder_open",
                    desc="Add or remove both sensor and background calibration preset",
                    to_address="/database"
                )