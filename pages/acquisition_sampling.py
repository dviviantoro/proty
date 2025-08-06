import os, sys
from nicegui import ui, run
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from pages.theme import frame
from modules.dictionary import *
from modules.database import tinydb_read, tinydb_append_xy, LMDBDict
from modules.template_ui import ToggleButtonAsync, grid_content_calibration, update_grid_content_calibration
# from modules.influxdb_inf import influx_write, influx_query
from modules.dsp import generate_sine
import asyncio
# import random

def update_appearance(timerange):
    print(f"execute from timer: {timerange}")

# def update_appearance(interval, timerange):


async def update_data(dict_temp, stop_event, run_event):
    try:
        while not stop_event.is_set():
            await run_event.wait()

            with LMDBDict() as db:
                retrieved_data = db.get("aqc")
                if retrieved_data["flag"]:
                    print("updating acquisition data")

                    for i in range(3):
                        dict_structure = {  
                            "measurement": "pd-test",
                            "tags": {
                                "name": dict_temp["name"],
                                "location": dict_temp["location"],
                                "phase": i+1,
                            },
                            "fields": retrieved_data[sensor_channels[i]]
                        }
                        run_process("write_influx", ["-d", json.dumps(dict_structure)])

                    retrieved_data["flag"] = False
                    db.put("aqc", retrieved_data)

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Update task cancelled.")
    finally:
        print("Update task finished.")

def stop_and_save(stop_event, charts, project):
    stop_event.set()
    for chart in charts:
        tinydb_append_xy("calibration", project, chart.options['dataset']['source'])
    ui.navigate.to("/")

def page() -> None:
    run_process("capture_scope", ["-t", "aqc", "-a", "1000", "-i", "1000"])


    # dict_r = create_dict_calibration("Calibration Sensor Phase R", [])
    # dict_s = create_dict_calibration("Calibration Sensor Phase S", [])
    # dict_t = create_dict_calibration("Calibration Sensor Phase T", [])
    dict_temp = tinydb_read("temp")[0]
    stop_event = asyncio.Event()
    run_event = asyncio.Event()
    run_event.clear()

    with frame("Oscilloscope Panel", "OK!"):
        with ui.tabs().classes('w-full') as tabs:
            tab_stream = ui.tab('Current Capture')
            tab_prpd = ui.tab('Phase Resolved Partial Discharge')
            tab_timeseries_value = ui.tab('Time Series of Value')
            tab_timeseries_count = ui.tab('Time Series of Count')
        with ui.tab_panels(tabs, value=tab_timeseries_value).classes('w-full'):
            # with ui.tab_panel(tab_stream):
            #     with ui.element('div').classes('grid grid-cols-12 w-full gap-1 mt-10 mb-10'):
            #         chart_r = ui.echart(options=dict_r).classes('h-[640px] col-start-1 col-span-8 size-full')
            #         with ui.card().classes('col-start-9 col-span-4 size-full'):
            #             ui.label('[Background Noise] My title is')
            #             code_r = ui.code(create_sentence("general_data", dict_temp, keys_acquisition, 0)).classes('w-full')
            #             grid_r = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
            #             with ui.row().classes("w-full place-content-center"):
            #                 ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_r, chart_r, code_r, dict_temp))
            # with ui.tab_panel(tab_prpd):
            #     with ui.element('div').classes('grid grid-cols-12 w-full gap-1 mt-10 mb-10'):
            #         chart_prpd = ui.echart(options=create_dict_prpd_3p([generate_sine(30, 0), generate_sine(30, 120), generate_sine(30, 240)], [])).classes('h-[640px] col-start-1 col-span-9 size-full')
            #         with ui.card().classes('col-start-10 col-span-3 size-full'):
            #             code_s = ui.code(create_sentence("general_data", dict_temp, keys_acquisition, 0)).classes('w-full')
            #             code_prpd = ui.code(create_sentence("prpd_data", dict_temp, keys_prpd, 0)).classes('w-full')
            #             # grid_s = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
            #             # with ui.row().classes("w-full place-content-center"):
            #             #     ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_s, chart_s, code_s, dict_temp))
            
            # WORKING ON THIS
            with ui.tab_panel(tab_timeseries_value):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-1 mt-10 mb-10'):
                    # chart_timeseries_value = ui.echart(options=echart_timeseries_value_3p([generate_sine(30, 0), generate_sine(30, 120), generate_sine(30, 240)])).classes('h-[640px] col-start-1 col-span-9 size-full')
                    chart_timeseries_value = ui.echart(options=echart_timeseries_value_3p([[], [], []])).classes('h-[640px] col-start-1 col-span-9 size-full')
                    with ui.card().classes('col-start-10 col-span-3 size-full'):
                        ui.label('[Background Noise] My title is')
                        summary_ts_value = ui.code(create_sentence("general_data", dict_temp, keys_acquisition, 0)).classes('w-full')
            with ui.tab_panel(tab_timeseries_count):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-1 mt-10 mb-10'):
                    chart_timeseries_count = ui.echart(options=echart_timeseries_count_3p([generate_sine(30, 0), generate_sine(30, 120), generate_sine(30, 240)])).classes('h-[640px] col-start-1 col-span-9 size-full')
                    with ui.card().classes('col-start-10 col-span-3 size-full'):
                        ui.label('[Background Noise] My title is')
                        code_t = ui.code(create_sentence("general_data", dict_temp, keys_acquisition, 0)).classes('w-full')
                        grid_t = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        # with ui.row().classes("w-full place-content-center"):
                        #     ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_t, chart_t, code_t, dict_temp))
        
        with ui.page_sticky(x_offset=18, y_offset=18, position="bottom-left"):
            with ui.row().classes("w-full place-content-center"):
                select_interval = ui.select(dict_interval, label="Interval", value=10)
                select_timerange = ui.select(dict_timerange, label="Timerange", value=60)
                
                timer_update = ui.timer(select_interval.value, lambda:update_appearance(select_timerange.value))
                select_interval.bind_value_to(timer_update, "interval")

        with ui.page_sticky(x_offset=18, y_offset=18, position="bottom"):
            with ui.row().classes("w-full place-content-center"):
                # charge = ui.number(label="Charge in pC")
                with ui.button_group():
                    ToggleButtonAsync(run_event)
                    ui.button(
                        "Stop and Save",
                        icon="stop_circle",
                        color="red",
                        # on_click= lambda: stop_and_save(stop_event, [chart_r, chart_s, chart_s], dict_temp["name"])
                    )
        
        with ui.page_sticky(x_offset=18, y_offset=18, position="bottom-right"):
            ui.button(icon='folder', on_click=lambda: ui.navigate.to("/database")).props('fab')

    asyncio.create_task(update_data(dict_temp, stop_event, run_event))