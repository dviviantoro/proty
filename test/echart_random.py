#!/usr/bin/env python3
from nicegui import ui
from datetime import datetime
import random

# ECharts options configuration
# This dictionary defines the structure and appearance of the chart.
# See the ECharts documentation for all possible options: https://echarts.apache.org/en/option.html
chart_options = {
    'title': {
        'text': 'Real-time IoT Sensor Data'
    },
    'tooltip': {
        'trigger': 'axis',
        'formatter': "function (params) {"
                     "  var date = new Date(params[0].value[0]);"
                     "  var data = params[0].value[1].toFixed(2);"
                     "  return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() + '<br/>' + data + ' °C';"
                     "}"
    },
    'xAxis': {
        'type': 'time',  # Critical for handling timestamps
        'splitLine': {
            'show': False
        }
    },
    'yAxis': {
        'type': 'value',
        'boundaryGap': [0, '10%'],
        'splitLine': {
            'show': True
        },
        'axisLabel': {
            'formatter': '{value} °C'
        }
    },
    'series': [{
        'name': 'Temperature',
        'type': 'line',
        'showSymbol': False,
        'hoverAnimation': False,
        'data': []  # Start with an empty list for data points
    }],
    'grid': {
        'left': '10%',
        'right': '10%',
        'bottom': '15%'
    },
    'dataZoom': [
        {
            'type': 'inside',
            'start': 50,
            'end': 100
        },
        {
            'start': 50,
            'end': 100
        }
    ]
}

# Create the UI
with ui.row().classes('w-full justify-center'):
    # The ui.echart element which will render the chart
    chart = ui.echart(chart_options).classes('w-full h-96')

# This list will hold our data points. In a real application,
# this might be fetched from a database or an API.
data_points = []
MAX_DATA_POINTS = 100 # Keep the last 100 data points to avoid crashing the browser

def update_chart():
    """
    This function is called by the timer to add new data to the chart.
    """
    # Get the current time in milliseconds since epoch, which ECharts understands
    timestamp = datetime.now().timestamp() * 1000
    print(type(timestamp))
    
    # Generate a random value to simulate a sensor reading (e.g., temperature)
    value = random.uniform(20.0, 25.0)
    
    # Add the new data point to our list
    data_points.append([timestamp, value])

    # To prevent the browser from slowing down, only keep the last N data points
    while len(data_points) > MAX_DATA_POINTS:
        data_points.pop(0)

    # Update the 'data' in the 'series' part of the chart options
    # NOTE: We access the series by its index (0 in this case)
    chart.options['series'][0]['data'] = data_points
    print(chart.options['series'][0]['data'])
    
    # Call the update method to refresh the chart in the browser
    chart.update()

# Use a ui.timer to call the update_chart function every 1 second (1000 ms)
# This simulates a real-time data feed from an IoT device.
ui.timer(5.0, update_chart)

ui.run()
