import theme
from nicegui import ui
from modules.sqlite3_interface import sqlite_read_table, sqlite_insert_data
from modules.dummy_data import *
from modules.dsp import *

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

    # regenerate sine
    new_sine = create_dummy_y(aligned_degree, 0.01)

    data_source = np.column_stack((aligned_degree, new_sine))
    data_sensor = np.column_stack((aligned_degree, filtered_sensor))
    data_sensor = data_sensor[~np.isnan(data_sensor).any(axis=1)]

    return data_sensor

def create_dict_pd():
    data_sine = generate_sine()
    data_sensor = call_dummy_pd(0.0048, -0.0045)
    dictionary = {
        "title": {"text": "Custom X-Axis for Each Series"},
        "tooltip": {"trigger": "item"},
        "legend": {"data": ["Series A", "Series B"]},
        "xAxis": {"type": "value", "name": "X"},
        "yAxis": {"type": "value", "name": "Y"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 30
        },
        "series": [
            {
                "name": "Phase Reference",
                "type": "line",
                "data": data_sine
            },
            {
                "name": "HFCT 1",
                "type": "scatter",
                "data": data_sensor
            }
        ]
    }
    return dictionary

def create_dict_charts():
    sine_data = generate_sine()
    dictionary = {
        "title": {"text": "Custom X-Axis for Each Series"},
        "tooltip": {"trigger": "item"},
        "legend": {"data": ["Series A", "Series B"]},
        "xAxis": {"type": "value", "name": "X"},
        "yAxis": {"type": "value", "name": "Y"},
        "grid": {
            "top": 40,
            "bottom": 40,
            "left": 60,
            "right": 30
        },
        "series": [
            {
                "name": "Series A",
                "type": "line",  # can also be 'scatter'
                "data": sine_data
            },
            {
                "name": "Series B",
                "type": "line",
                "data": [
                    [1, 8],
                    [3, 6],
                    [5, 12]
                ]
            }
        ]
    }
    return dictionary

# tab phase resolve
# tab historical

def scope_page() -> None:
    with theme.frame("Oscilloscope Panel", "OK!"):
        # with ui.element('div').classes('grid grid-cols-12 absolute-center w-full gap-1 h-96'):
        with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-16 mb-16'):
            # with ui.element('div').style('height: 200px;').classes('col-start-1 col-span-8 h-150'):
            with ui.element('div').classes('col-start-1 col-span-8 size-full'):
                with ui.tabs().classes('w-full') as tabs:
                    tab_pr = ui.tab('Phase Resolved')
                    tab_history = ui.tab('Historical')
                with ui.tab_panels(tabs, value=tab_pr).classes('w-full'):
                    with ui.tab_panel(tab_pr):
                        # ui.echart(options=create_dict_charts(), on_point_click=ui.notify).classes('h-[640px] w-full')
                        ui.echart(options=create_dict_pd(), on_point_click=ui.notify).classes('h-[640px] w-full')
                    with ui.tab_panel(tab_history):
                        ui.echart(options=create_dict_charts(), on_point_click=ui.notify).classes('h-[320px] w-full')
                        ui.echart(options=create_dict_charts(), on_point_click=ui.notify).classes('h-[320px] w-full')
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
                        with ui.button(color="#47C483"):
                            ui.label("Add Point").style("color: white")
                            ui.spinner(size='lg')
                    with ui.tab_panel(tab_result):
                        ui.label('Second tab')










        # with ui.tabs().classes('w-full') as tabs:
        #     one = ui.tab('One')
        #     two = ui.tab('Two')
        # with ui.tab_panels(tabs, value=two).classes('w-full'):
        #     with ui.tab_panel(one):
        #         with ui.element('div').classes('grid grid-cols-12 absolute-center w-full gap-1 h-96'):
        #             with ui.element('div').classes('col-start-1 col-span-8 h-96'):
        #                 create_charts()
        #     with ui.tab_panel(two):
        #         ui.label('Second tab')


                # with ui.element('div').classes('grid grid-cols-11 absolute-center w-full gap-5 col-start-2 col-span-5'):


        #         with ui.element('div').classes('grid grid-cols-12 absolute-center w-full gap-5'):
        #             with ui.card().style("border: none; background-color: transparent;").classes('no-shadow col-start-1 col-span-6 h-52'):
        #                 with ui.element('div').classes('grid grid-cols-11 absolute-center w-full gap-5'):
        #                     ui.label('First tab')
        #                     create_charts()

