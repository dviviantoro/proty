import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.template_ui import generate_step, grid_content, update_grid_content
from modules.database import tinydb_insert_dict, tinydb_check_existence, tinydb_read
from pages.theme import frame
from modules.util import *

def go_sampling():
    dict_temp = tinydb_read("temp")[0]
    if tinydb_check_existence("calibration_sampling", dict_temp["name"]):
        ui.notify('Calibration preset name you entered is exist, please change it!', type='warning')
    else:
        dict_acquisition = {}
        for key in keys_acquisition:
            dict_acquisition[key] = dict_temp[key]
        tinydb_insert_dict("aqcuisition", dict_acquisition)
        ui.navigate.to("/acquisition_sampling")

def page() -> None:
    with frame("Acquisition Panel", 'You have to turn on all services'):
        with ui.element('div').classes('absolute-center w-[1080px]'):
            with ui.stepper().props('horizontal') as stepper:
                operator = generate_step(
                    stepper=stepper,
                    step_title="Operator",
                    step_label="Write your name to make the next step easier",
                    input_type="input"
                )
                name = generate_step(
                    stepper=stepper,
                    step_title="Title",
                    step_label="Name the title of calibration preset",
                    input_type="input"
                )
                location = generate_step(
                    stepper=stepper,
                    step_title="Loc",
                    step_label="Name the location you are trying to calibrate the sensors",
                    input_type="input"
                )
                sensor = generate_step(
                    stepper=stepper,
                    step_title="Sensor",
                    step_label="Select the sensor from the list below",
                    input_type="dropdown-sensor"
                )
                background = generate_step(
                    stepper=stepper,
                    step_title="Bgn",
                    step_label="Select the calibrator from the list below",
                    input_type="dropdown-background"
                )
                calibration = generate_step(
                    stepper=stepper,
                    step_title="Cal",
                    step_label="Select the calibrator from the list below",
                    input_type="dropdown-calibration"
                )
                phase_ref = generate_step(
                    stepper=stepper,
                    step_title="PhaseRef",
                    step_label="Select the calibrator from the list below",
                    input_type="dropdown-phase"
                )

                with ui.step("Review"):
                    with ui.row().classes("w-full place-content-center"):
                        ui.label("Please review your collected data before to start sampling").style('text-align: center;')
                    with ui.row().classes("w-full place-content-center"):
                        grid = ui.aggrid(grid_content()).classes('h-[240px] w-[320px]')
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
                                        "sensor": sensor.value,
                                        "background": background.value,
                                        "calibration": calibration.value,
                                        "phase_ref": phase_ref.value
                                    }
                                )
                            ): ui.label("Review Data").style("color: white")
                            with ui.button(
                                color="#47C483",
                                on_click= lambda: go_sampling()
                            ): ui.label("Go Sampling").style("color: white")
