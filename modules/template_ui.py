import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import tinydb_read, tinydb_update_temp
from modules.util import *

def check_input(input, stepper):
    stepper.next() if input else ui.notify('plese input your data', type='warning')

def generate_option(input_type):
    option = []
    category = input_type.split("-")[1]
    datas = tinydb_read(category)
    for data in datas:
        option.append(data["name"])
    return option

def grid_database():
    grid_content = {
        'columnDefs': [
            {'headerName': 'Category', 'field': 'category', 'filter': 'agTextColumnFilter', 'floatingFilter': True, "flex": 1},
            {'headerName': 'Created', 'field': 'timestamp', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Project', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Operator', 'field': 'operator', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Location', 'field': 'location', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Sensor', 'field': 'sensor', 'filter': 'agTextColumnFilter', 'floatingFilter': True}
        ],
        'rowSelection': 'single',
    }
    return grid_content

# def update_grid_database():


def grid_content_calibration():
    grid_content = {
        'defaultColDef': {'flex': 1},
        'columnDefs': [
            {'headerName': 'Voltage (mV)', 'field': 'voltage', 'checkboxSelection': True},
            {'headerName': 'Charge (pC)', 'field': 'charge'},
        ],
        'rowSelection': 'multiple',
    }
    return grid_content

def update_grid_content_calibration(grid, voltages, charges):
    rows = []
    for voltage, charge in zip(voltages, charges):
        rows.append({"voltage": voltage, "charge": charge})
    grid.options["rowData"] = rows
    grid.update()

def grid_content():
    grid_content = {
        'defaultColDef': {'flex': 1},
        'columnDefs': [
            {'headerName': 'Parameter', 'field': 'param'},
            {'headerName': 'Value', 'field': 'val'},
        ],
        'rowSelection': 'multiple',
    }
    return grid_content

def update_grid_content(grid, data):
    rows = []
    for key, value in data.items():
        rows.append({"param": key, "val": value})
    grid.options["rowData"] = rows
    grid.update()

    # store to db
    now_datetime = datetime.now()
    formatted_string = now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data["timestamp"] = formatted_string
    data["xy"] = []
    for key in list(data.keys()):
        tinydb_update_temp(key, data[key])
        logger.info(f"temp data changed = {key}: {data[key]}")

def generate_step(stepper, step_title:str, step_label:str, input_type:str):
    with ui.step(step_title):
        with ui.row().classes("w-full place-content-center"):
            ui.label(step_label).style('text-align: center;')
        with ui.row().classes("w-full place-content-center"):
            if input_type == "input":
                my_input = ui.input(placeholder='type here').props('rounded outlined dense')
            else:
                my_input = ui.select(label="Option selection", options=generate_option(input_type)).classes("w-64")
        with ui.row().classes("w-full place-content-center"):
            with ui.stepper_navigation():
                if step_title != "Operator":
                    with ui.button(color="#FDE9A0", on_click=stepper.previous):
                        ui.label("Back").style("color: #494848")
                with ui.button(color="#47C483", on_click=lambda:check_input(my_input.value, stepper)):
                    ui.label("Next").style("color: white")
    return my_input

class ToggleButtonAsync(ui.button):
    def __init__(self, target_event, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._target = target_event
        # self._state = self._target.is_set
        self._state = False
        self.on('click', self.toggle)
        self.update_appearance()
    def toggle(self) -> None:
        self._state = not self._state
        if self._state:
            self._target.set()
        else:
            self._target.clear()
        self.update_appearance()
    def update_appearance(self) -> None:
        if self._state:
            self.text = 'Pause'
            self.props('color=blue icon=pause_circle')
        else:
            self.text = 'Start'
            self.props('color=green icon=play_circle')


def check_phase(to_address):
    dict_temp = tinydb_read("temp")[0]
    if dict_temp["phase"]:
        ui.navigate.to(to_address)
    else:
        ui.notify("Please select phase number on the top of home page", type="warning")

def slide_phase_reset(slide):
    slide.reset()
    tinydb_update_temp("phase", False)

def slide_phase_swiped(message, phase):
    ui.notify(message, type="positive")
    tinydb_update_temp("phase", phase)

def generate_main_button(size:str, title:str, icon:str, desc:str, to_address:str):
    with ui.button(color="#3874c8",  on_click=lambda:check_phase(to_address)).classes(size).style('height: 450px;').props("fab"):
        with ui.row().classes("w-full place-content-center"):
            ui.label(title).classes('text-2xl font-bold').style("color: white")
        with ui.row().classes("w-full place-content-center"):
            ui.icon(name=icon, size="8rem").style("color: white")
        with ui.row().classes("w-full place-content-center"):
            ui.label(desc).style('text-align: center; padding-bottom: 20px; color: white;')