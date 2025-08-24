from nicegui import ui, app

active_input = None
shift_on = False
caps_lock_on = False
keyboard_visible = False

ui.button.default_props('no-caps')
keyboard_container = ui.row()

# --- Logic Functions ---
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
    """Toggles the shift key state."""
    global shift_on
    if force_off is not None:
        if shift_on == force_off: return
        shift_on = force_off
    else:
        shift_on = not shift_on
    
    build_keyboard.refresh()
    
def toggle_caps_lock():
    """Toggles the caps lock state."""
    global caps_lock_on
    caps_lock_on = not caps_lock_on
    # When Caps Lock is toggled, also reset the shift key state
    toggle_shift(force_off=False)

def on_input_focus(e):
    """Sets the active input and shows the keyboard."""
    global active_input, keyboard_visible
    active_input = e.sender
    keyboard_visible = True
    ui.update()

def build_keyboard():
    with ui.column().classes('w-full items-center'):
        with ui.row().classes('justify-center w-full gap-1'):
            for key in '1234567890':
                ui.button(key, on_click=lambda k=key: add_char(k)).classes('text-lg')
        with ui.row().classes('justify-center w-full gap-1'):
            for key in 'qwertyuiop':
                ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('text-lg')
        with ui.row().classes('justify-center w-full gap-1'):
            for key in 'asdfghjkl':
                ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('text-lg')
        with ui.row().classes('justify-center w-full gap-1'):
            ui.button('⇧', on_click=lambda: toggle_shift()).props('color=primary' if shift_on else '')
            for key in 'zxcvbnm':
                ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('text-lg')
            ui.button('⌫', on_click=delete_char)
        with ui.row().classes('justify-center w-full mt-2 gap-1'):
            ui.button('CAPS', on_click=lambda: toggle_caps_lock()).props('color=primary' if caps_lock_on else 'color=secondary')
            ui.button('Space', on_click=lambda: add_char(' ')).classes('w-48 text-lg')


# Your main page content
ui.label('Tap on an input field to open the keyboard').classes('text-2xl mt-8')

# Your input fields that will use the on-screen keyboard
ui.input(label='Enter username').classes('w-full').on('focus', on_input_focus)
ui.input(label='Enter password', password=True).classes('w-full').on('focus', on_input_focus)

with ui.column().classes('fixed bottom-0 left-1/2 -translate-x-1/2 p-2 z-10'):
    build_keyboard()

ui.run()