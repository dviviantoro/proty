from nicegui import ui

ui.label('Move the slider to change the timer speed:')
# Create a slider to control the interval from 0.1s to 2.0s
slider = ui.slider(min=0.1, max=2.0, step=0.1, value=1.0).props('label-always')

# Display the current timer interval
ui.label().bind_text_from(slider, 'value', lambda v: f'Interval: {v:.1f} s')

# Initialize a counter
count = 0
counter_label = ui.label(f'Count: {count}')

def update_counter():
    """Increments and updates the counter label."""
    global count
    count += 1
    counter_label.set_text(f'Count: {count}')

# Create the timer with an initial interval
timer = ui.timer(1.0, update_counter)

# THIS IS THE CORRECTED LINE:
# Bind the slider's value to the timer's interval property.
slider.bind_value_to(timer, 'interval')

ui.run()