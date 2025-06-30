# di page ini hanya ditampilkan PRPD last 1 minute, 5 minute, 10 minute
# untuk keseluruhan nanti ditampilkan di database

import theme
from nicegui import ui
from modules.sqlite3_interface import sqlite_read_table, sqlite_insert_data
from modules.dummy_data import *
from modules.dsp import *
from modules.dictionary import *
import asyncio
import random
from datetime import datetime

source_path = "/Users/deny/proty02/assets/csv/sample2/pfugsumber.csv"
sensor_path = "/Users/deny/proty02/assets/csv/sample2/pfugrc.csv"

def generate_sine(amplitude = 0.01):
    x_axis = np.linspace(0, 360, 360, endpoint=False)
    y_axis = amplitude * np.sin(np.radians(x_axis))
    return np.column_stack((x_axis, y_axis))

def call_dummy_pd(max_filter, min_filter):
    # call data
    x_source, y_source = create_dummy_data(source_path)
    x_sensor, y_sensor = create_dummy_data(sensor_path)

    # filter noise
    filtered_sensor = filter_noise(y_sensor, max_filter, min_filter)

    # align source degree
    aligned_degree = align_degree(y_source, 3.5)

    data_sensor = np.column_stack((aligned_degree, filtered_sensor))
    return data_sensor[~np.isnan(data_sensor).any(axis=1)]

async def update_chart(chart):
    while True:
        now = datetime.now()
        random_pos = random.randint(1, 10)
        random_neg = random.randint(-10, -1)
        chart.options['dataset']['source'].append([now, random_pos, random_neg])
        chart.update()
        await asyncio.sleep(1)

def scope_page() -> None:
    
    with theme.frame("Oscilloscope Panel", "OK!"):
        with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-16 mb-16'):
            with ui.element('div').classes('col-start-1 col-span-8 size-full'):
                with ui.tabs().classes('w-full') as tabs:
                    tab_pr = ui.tab('Phase-Based')
                    tab_history = ui.tab('Time-Based')
                with ui.tab_panels(tabs, value=tab_history).classes('w-full'):
                    with ui.tab_panel(tab_pr):
                        data_sine = generate_sine()
                        data_sensor = call_dummy_pd(0.0048, -0.0045)
                        ui.echart(options=create_dict_prpd(data_sine, data_sensor)).classes('h-[640px] w-full')
                    with ui.tab_panel(tab_history):
                        dict_max_charge = create_dict_historical("Max Charge", "Charge (pC)", [])
                        dict_n_charge = create_dict_historical("Num Charge", "Count", [])
                        chart_max_charge = ui.echart(options=dict_max_charge).classes('h-[320px] w-full')
                        chart_n_charge = ui.echart(options=dict_n_charge).classes('h-[320px] w-full')
                        asyncio.create_task(update_chart(chart_max_charge))
                        asyncio.create_task(update_chart(chart_n_charge))
            with ui.card().classes('no-shadow col-start-9 col-span-4 size-full'):
                with ui.tabs().classes('w-full') as tabs:
                    tab_config = ui.tab('Config')
                    tab_result = ui.tab('Results')
                with ui.tab_panels(tabs, value=tab_config).classes('w-full'):
                    with ui.tab_panel(tab_config):
                        ui.label('[Background Noise] My title is')
                        ui.label('Welcome to Background Noise Panel')
                        ui.label('Please make sure you have done following check list below:')
                        checkbox_sensor1 = ui.checkbox('Sensor 1 plugged on Channel 2')
                        checkbox_sensor2 = ui.checkbox('Sensor 2 plugged on Channel 3')
                        checkbox_sensor3 = ui.checkbox('Sensor 3 plugged on Channel 4')
                        checkbox_environment = ui.checkbox('All sensors facing background conditions')
                        ui.label('Number of iteration')
                        slider_iteration = ui.slider(min=0, max=20, value=5).props('label-always')
                        with ui.button(color="#47C483", on_click=update_chart):
                            ui.label("Add Point").style("color: white")
                            ui.spinner(size='lg')
                    with ui.tab_panel(tab_result):
                        ui.label('Second tab')
