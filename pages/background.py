import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.template_ui import generate_step, grid_content, update_grid_content
from modules.database import tinydb_insert_dict, tinydb_check_existence, tinydb_read
from pages.theme import frame
from modules.util import *

def go_sampling():
    dict_temp = tinydb_read("temp")[0]
    if tinydb_check_existence("background", dict_temp["name"]):
        ui.notify('Background preset name you entered is exist, please change it!', type='warning')
    else:
        dict_background = {"xy": []}
        for key in keys_background:
            dict_background[key] = dict_temp[key]
        tinydb_insert_dict("background", dict_background)
        ui.navigate.to("/background_sampling")

def page() -> None:
    with frame("Background Sampling Panel", 'You have to turn on all services'):
        with ui.element('div').classes('grid-cols-12 absolute-center gap-10'):
            with ui.stepper().props('horizontal') as stepper:
                operator = generate_step(
                    stepper=stepper,
                    step_title="Operator",
                    step_label="Write your name to make the next step easier",
                    input_type="input"
                )
                name = generate_step(
                    stepper=stepper,
                    step_title="Name Project",
                    step_label="Name the project of background sampling process",
                    input_type="input"
                )
                location = generate_step(
                    stepper=stepper,
                    step_title="Location",
                    step_label="Name the location you are trying to sampling the background",
                    input_type="input"
                )
                sensor = generate_step(
                    stepper=stepper,
                    step_title="Sensor",
                    step_label="Select the sensor from the list below",
                    input_type="dropdown-sensor"
                )

                with ui.step("Review"):
                    with ui.row().classes("w-full place-content-center"):
                        ui.label("Please review your collected data before to start sampling").style('text-align: center;')
                    with ui.row().classes("w-full place-content-center"):
                        grid = ui.aggrid(grid_content()).classes('max-h-40')
                    with ui.row().classes("w-full place-content-center"):
                        with ui.stepper_navigation():
                            with ui.button(color="#FDE9A0", on_click=stepper.previous):
                                ui.label("Back").style("color: #494848")
                            with ui.button(
                                color="#3874c8",
                                on_click= lambda: update_grid_content(grid,
                                    {
                                        "operator": operator.value,
                                        "name": name.value,
                                        "location": location.value,
                                        "sensor": sensor.value
                                    }
                                )
                            ): ui.label("Review Data").style("color: white")
                            with ui.button(
                                color="#47C483",
                                on_click= lambda: go_sampling()
                            ): ui.label("Go Sampling").style("color: white")