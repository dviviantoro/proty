import os, sys, signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from pages.theme import frame
from modules.dictionary import *
from modules.database import tinydb_read, tinydb_append_xy, LMDBDict
from modules.template_ui import ToggleButtonAsync
import asyncio

async def update_appearance(stop_event, run_event, charts, summary):
    try:
        while not stop_event.is_set():
            await run_event.wait()

            with LMDBDict() as db:
                retrieved_data = db.get("bgn")
                if retrieved_data["flag"]:
                    channels = ["ch2", "ch3", "ch4"]
                    collected_data = []

                    for i in range(0,3):
                        n = len(charts[i].options['dataset']['source'])
                        charts[i].options['dataset']['source'].append([n + 1, retrieved_data[channels[i]]["max"], retrieved_data[channels[i]]["min"]])
                        collected_data.append(charts[i].options['dataset']['source'])
                        charts[i].update()

                    general_data = generate_string_general("general", tinydb_read("temp")[0], keys_background)
                    bgn_data = summary_bgn(collected_data)
                    full_summary = general_data + bgn_data
                    summary.set_content(full_summary)
                    retrieved_data["flag"] = False
                    db.put("bgn", retrieved_data)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Update task cancelled.")
    finally:
        print("Update task finished.")

def stop_and_save(stop_event, charts):
    stop_event.set()

    dict_temp = tinydb_read("temp")[0]
    os.kill(dict_temp["pid_capture"], signal.SIGTERM)
    os.kill(dict_temp["pid_scope"], signal.SIGTERM)

    for chart in charts:
        data = chart.options['dataset']['source']
        new_data = [item[1:] for item in data]
        # print(new_data)
        tinydb_append_xy("background", dict_temp["name"], new_data)
    ui.navigate.to("/")

def page() -> None:
    run_process("capture_scope", ["-t", "bgn"])

    dict_r = create_dict_counter_background("Background Noise Sensor R", "Voltage (mv)", [])
    dict_s = create_dict_counter_background("Background Noise Sensor S", "Voltage (mv)", [])
    dict_t = create_dict_counter_background("Background Noise Sensor T", "Voltage (mv)", [])
    
    stop_event = asyncio.Event()
    run_event = asyncio.Event()
    run_event.clear()

    with frame("Oscilloscope Panel", "OK!"):
        with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-16 mb-16'):
            with ui.card().classes('no-shadow col-start-1 col-span-8 size-full'):
                chart_r = ui.echart(options=dict_r).classes('h-[250px] w-full')
                chart_s = ui.echart(options=dict_s).classes('h-[250px] w-full')
                chart_t = ui.echart(options=dict_t).classes('h-[250px] w-full')
            with ui.card().classes('no-shadow col-start-9 col-span-4 size-full'):
                ui.label('[Background Noise] My title is')
                summary = ui.code("hello world!").classes('w-full')
                with ui.row().classes("w-full place-content-center"):
                    ToggleButtonAsync(run_event)
                    ui.button(
                        "Stop and Save",
                        icon="stop_circle",
                        color="red",
                        on_click= lambda: stop_and_save(stop_event, [chart_r, chart_s, chart_s])
                    )

    asyncio.create_task(update_appearance(stop_event, run_event, [chart_r, chart_s, chart_t], summary))