import os, sys
from nicegui import ui, app

# NOTE: Your original imports are preserved below, but for this example to run
# they are commented out as we don't have access to your modules.
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from modules.template_ui import generate_step, grid_content, update_grid_content
# from modules.database import tinydb_insert_dict, tinydb_check_existence, tinydb_read
# from pages.theme import frame
# from modules.util import *

# ================================================
# Key logic and UI components for the keyboard
# ================================================
active_input = None
shift_on = False
caps_lock_on = False
keyboard_visible = False

def add_char(char):
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
    global active_input
    if active_input and active_input.value:
        active_input.value = active_input.value[:-1]
        
def toggle_shift(force_off=None):
    global shift_on
    if force_off is not None:
        if shift_on == force_off: return
        shift_on = force_off
    else:
        shift_on = not shift_on
    build_keyboard.refresh()
    
def toggle_caps_lock():
    global caps_lock_on
    caps_lock_on = not caps_lock_on
    toggle_shift(force_off=False)

def close_keyboard():
    global active_input, keyboard_visible, shift_on, caps_lock_on
    active_input = None
    keyboard_visible = False
    shift_on = False
    caps_lock_on = False
    ui.update()

def on_input_focus(e):
    global active_input, keyboard_visible
    active_input = e.sender
    keyboard_visible = True
    ui.update()

# ================================================
# Simplified functions to make the code runnable
# ================================================
def generate_step(stepper, step_title, step_label, input_type):
    with ui.step(step_title).props(f'caption="{step_label}"'):
        if input_type == "input":
            input_field = ui.input(label=step_title).classes('w-full').on('focus', on_input_focus)
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous).props('flat')
            return input_field
        else:
            ui.label(f"This is a {input_type} field")
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous).props('flat')
            return ui.select(label=step_title, options=['Sensor A', 'Sensor B']).classes('w-full')

def go_sampling():
    ui.notify("Starting sampling process...")

def update_grid_content(grid, data):
    grid.options['rowData'] = [data]
    grid.update()

def grid_content():
    return [{"operator": "", "name": "", "location": "", "sensor": ""}]

def frame(title, description):
    def decorator(func):
        def wrapper():
            with ui.header(elevated=True).style('background-color: #3874c8'):
                ui.label(title).classes('text-3xl font-bold tracking-tight')
            ui.label(description).classes('text-2xl mt-8')
            func()
            with ui.footer(elevated=True):
                ui.label('Powered by NiceGUI')
        return wrapper
    return decorator
# ================================================
# Main page function with keyboard integration
# ================================================

@ui.page('/background_sampling')
def page() -> None:
    # Keyboard UI is a fixed element, so it must be outside the frame
    with ui.column().classes('fixed bottom-0 left-1/2 -translate-x-1/2 p-2 bg-gray-200 z-10').bind_visibility_from(locals(), 'keyboard_visible'):
        @ui.refreshable
        def build_keyboard():
            with ui.column().classes('w-full items-center'):
                # First row of numbers
                with ui.row().classes('justify-center w-full gap-1'):
                    for key in '1234567890':
                        ui.button(key, on_click=lambda k=key: add_char(k)).classes('text-lg')

                # Second row (QWERTY)
                with ui.row().classes('justify-center w-full gap-1'):
                    for key in 'qwertyuiop':
                        ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('text-lg')

                # Third row
                with ui.row().classes('justify-center w-full gap-1'):
                    for key in 'asdfghjkl':
                        ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('text-lg')

                # Fourth row
                with ui.row().classes('justify-center w-full gap-1'):
                    ui.button('⇧', on_click=lambda: toggle_shift()).props('color=primary' if shift_on else '')
                    for key in 'zxcvbnm':
                        ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('text-lg')
                    ui.button('⌫', on_click=delete_char)

                # Special function keys
                with ui.row().classes('justify-center w-full mt-2 gap-1'):
                    ui.button('CAPS', on_click=lambda: toggle_caps_lock()).props('color=primary' if caps_lock_on else 'color=secondary')
                    ui.button('Space', on_click=lambda: add_char(' ')).classes('w-48 text-lg')
                    ui.button('Done', on_click=close_keyboard).props('flat')
    
    # Initial call to build the keyboard
    build_keyboard()
    
    # Original frame and stepper content from your code
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

ui.run()