from nicegui import ui, app

# A variable to store the currently active input field
active_input = None
# A variable to track the shift state for a single character
shift_on = False
# A new variable to track the Caps Lock state
caps_lock_on = False
# A variable to control the visibility of the keyboard
keyboard_visible = False

ui.button.default_props('no-caps')
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

# --- UI Layout and Building ---

# This is our keyboard container with the corrected centering classes
# with ui.column().classes('fixed bottom-0 left-1/2 -translate-x-1/2 p-2 bg-gray-200 z-10').bind_visibility_from(locals(), 'keyboard_visible'):
with ui.column().classes('fixed bottom-0 left-1/2 -translate-x-1/2 p-2 z-10').bind_visibility_from(locals(), 'keyboard_visible'):
    
    # We decorate the function to make it refreshable
    @ui.refreshable
    def build_keyboard():
        with ui.column().classes('w-full items-center'):
            # First row of numbers
            with ui.row().classes('justify-center w-full gap-1'):
                for key in '1234567890':
                    ui.button(key, on_click=lambda k=key: add_char(k)).classes('w-12 text-lg')

            # Second row (QWERTY)
            with ui.row().classes('justify-center w-full gap-1'):
                for key in 'qwertyuiop':
                    ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')

            # Third row
            with ui.row().classes('justify-center w-full gap-1'):
                for key in 'asdfghjkl':
                    ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')

            # Fourth row
            with ui.row().classes('justify-center w-full gap-1'):
                ui.button('⇧', on_click=lambda: toggle_shift()).props('color=primary' if shift_on else '')
                for key in 'zxcvbnm':
                    ui.button(key.upper() if caps_lock_on or shift_on else key, on_click=lambda k=key: add_char(k)).classes('w-16 text-lg')
                ui.button('⌫', on_click=delete_char)

            # Special function keys
            with ui.row().classes('justify-center w-full mt-2 gap-1'):
                # Using a regular button with conditional props again
                ui.button('caps', on_click=lambda: toggle_caps_lock()).props('flat')
                ui.button('space', on_click=lambda: add_char(' ')).classes('w-72 text-lg')
                ui.button('hide', on_click=close_keyboard).props('flat')
    
    # We build the keyboard initially by calling the refreshable function
    build_keyboard()

# Your main page content
ui.label('Tap on an input field to open the keyboard').classes('text-2xl mt-8')

# Your input fields that will use the on-screen keyboard
ui.input(label='Enter username').classes('w-full').on('focus', on_input_focus)
ui.input(label='Enter password', password=True).classes('w-full').on('focus', on_input_focus)

ui.run()