from nicegui import ui
from picoscope_stream import initialize_scope, get_latest_data
from data_buffer import data_buffer
import asyncio

# Initialize the PicoScope device
initialize_scope()

# Set up a page
ui.label("📈 Real-Time PicoScope Stream")

# Create ECharts element
chart = ui.echart({
    'title': {'text': 'Channel A (Streaming)'},
    'tooltip': {'trigger': 'axis'},
    'xAxis': {'type': 'category', 'data': []},
    'yAxis': {'type': 'value'},
    'series': [{
        'name': 'Channel A',
        'type': 'line',
        'data': [],
        'showSymbol': False,
        'hoverAnimation': False,
    }]
}).classes('w-full h-96')

# Define an async loop to update chart
async def update_chart():
    while True:
        get_latest_data()  # Fetch new data from PicoScope
        x = data_buffer['x_data']
        y = data_buffer['y_data']
        if x and y:
            chart.options['xAxis']['data'] = x
            chart.options['series'][0]['data'] = y
            chart.update()
        await asyncio.sleep(0.1)  # Update every 100ms

# Launch chart updater
ui.run_with(asyncio.create_task(update_chart()))

# Run NiceGUI app
ui.run()
