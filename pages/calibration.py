import os, sys
from nicegui import ui
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from modules.template_ui import generate_step, grid_content, update_grid_content
from modules.template_ui import generate_option, check_input, grid_content, update_grid_content
from modules.database import tinydb_insert_dict, tinydb_check_existence, tinydb_read
from pages.theme import frame
from modules.util import *

active_input = None
shift_on = False
caps_lock_on = False
keyboard_visible = False
keyboard_container = ui.row()

def add_char(char):
    """Appends a character to the active input field."""
    global active_input, shift_on, caps_lock_on
    if active_input:
        if caps_lock_on:
            active_input.value += char.upper()
        elif shift_on:
            active_input.value += char.upper()
            toggle_shift(force_off=True)
        else:
            active_input.value += char.lower()
        
def delete_char():
    """Removes the last character from the active input field."""
    global active_input
    if active_input and active_input.value:
        active_input.value = active_input.value[:-1]
        
def toggle_shift(force_off=None):
    """Toggles the shift key state and rebuilds the keyboard UI."""
    global shift_on
    if force_off is not None:
        if shift_on == force_off: return
        shift_on = force_off
    else:
        shift_on = not shift_on
    keyboard_container.clear()
    with keyboard_container:
        build_keyboard()
    ui.update(keyboard_container)
    
def toggle_caps_lock():
    """Toggles the caps lock state."""
    global caps_lock_on
    caps_lock_on = not caps_lock_on
    toggle_shift(force_off=False)

def close_keyboard():
    """Hides the keyboard and clears the active input."""
    global active_input, keyboard_visible, shift_on, caps_lock_on
    active_input = None
    keyboard_visible = False
    shift_on = False
    caps_lock_on = False
    ui.update()

def on_input_focus(e):
    """Sets the active input and shows the keyboard."""
    global active_input, keyboard_visible
    active_input = e.sender
    keyboard_visible = True
    ui.update()

def build_keyboard():
    with ui.column().classes('w-full items-center gap-1'):
        with ui.row().classes('justify-center w-full gap-1'):
            for key in '1234567890':
                ui.button(key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')
        with ui.row().classes('justify-center w-full gap-1'):
            for key in 'qwertyuiop':
                ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')
        with ui.row().classes('justify-center w-full gap-1'):
            for key in 'asdfghjkl':
                ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')
        with ui.row().classes('justify-center w-full gap-1'):
            ui.button('caps', on_click=lambda: toggle_caps_lock())
            for key in 'zxcvbnm':
                ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')
            ui.button('⌫', on_click=delete_char)
        with ui.row().classes('justify-center w-full mt-2 gap-1'):
            ui.button('Space', on_click=lambda: add_char(' ')).classes('w-80 text-lg')

def next_step(value, stepper):
    check_input(value, stepper)
    close_keyboard()

def generate_step(stepper, step_title:str, step_label:str, input_type:str):
    with ui.step(step_title):
        with ui.row().classes("w-full place-content-center"):
            ui.label(step_label).style('text-align: center;')
        with ui.row().classes("w-full place-content-center"):
            if input_type == "input":
                my_input = ui.input(label=step_title).on('focus', on_input_focus).props('rounded outlined dense')
            else:
                my_input = ui.select(label="Option selection", options=generate_option(input_type)).classes("w-64")
        with ui.row().classes("w-full place-content-center"):
            with ui.stepper_navigation():
                if step_title != "Operator":
                    with ui.button(color="#FDE9A0", on_click=stepper.previous):
                        ui.label("Back").style("color: #494848")
                with ui.button(color="#47C483", on_click=lambda:next_step(my_input.value, stepper)):
                    ui.label("Next").style("color: white")
    return my_input

def go_sampling():
    dict_temp = tinydb_read("temp")[0]
    if tinydb_check_existence("calibration_sampling", dict_temp["name"]):
        ui.notify('Calibration preset name you entered is exist, please change it!', type='warning')
    else:
        dict_calibration = {"xy": []}
        for key in keys_calibration:
            dict_calibration[key] = dict_temp[key]
        tinydb_insert_dict("calibration", dict_calibration)
        ui.navigate.to("/calibration_sampling")

def page() -> None:
    with frame("Calibration Sampling Panel", 'You have to turn on all services'):
        with ui.column().classes('fixed bottom-5 left-1/2 -translate-x-1/2 p-2 z-10').bind_visibility_from(globals(), 'keyboard_visible'):
            build_keyboard()
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
                calibrator = generate_step(
                    stepper=stepper,
                    step_title="Cal",
                    step_label="Select the calibrator from the list below",
                    input_type="dropdown-calibrator"
                )
                background = generate_step(
                    stepper=stepper,
                    step_title="Bgn",
                    step_label="Select background preset from the list below",
                    input_type="dropdown-background"
                )

                with ui.step("Review"):
                    with ui.row().classes("w-full place-content-center"):
                        ui.label("Please review your collected data before to start sampling").style('text-align: center;')
                    with ui.row().classes("w-full place-content-center"):
                        grid = ui.aggrid(grid_content()).classes('max-h-[220px]')
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
                                        "calibrator": calibrator.value,
                                        "background": background.value,
                                    }
                                )
                            ): ui.label("Review Data").style("color: white")
                            with ui.button(
                                color="#47C483",
                                on_click= lambda: go_sampling()
                            ): ui.label("Go Sampling").style("color: white")
