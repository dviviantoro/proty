import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from pages.theme import frame
from modules.dictionary import *
from modules.database import tinydb_read, tinydb_append_xy
from modules.template_ui import ToggleButtonAsync

from modules.dsp import *
import asyncio
import random

# async def update_appearance(data, chart, summary, stop_event, run_event):
async def update_appearance(charts, stop_event, run_event):
    try:
        while not stop_event.is_set():
            await run_event.wait()
            
            random_pos = random.randint(1, 10)
            random_neg = random.randint(-10, -1)

            for chart in charts:
                n = len(chart.options['dataset']['source'])
                chart.options['dataset']['source'].append([n + 1, random_pos, random_neg])
                chart.update()


            # chart.options['dataset']['source'].append([n, random_pos, random_neg])
            # chart.update()

            # summary.set_content(
            #     create_summary_background(
            #         data,
            #         n,
            #         (random_pos+random_neg)/2,
            #         random_pos,
            #         random_neg,
            #         (random_pos+random_neg)/2,
            #         random_pos,
            #         random_neg,
            #         (random_pos+random_neg)/2,
            #         random_pos,
            #         random_neg
            #         )
            #     )
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Update task cancelled.")
    finally:
        print("Update task finished.")

def stop_and_save(stop_event, charts, project):
    stop_event.set()

    for chart in charts:
        data = chart.options['dataset']['source']
        new_data = [item[1:] for item in data]
        print(new_data)
        tinydb_append_xy("background_sampling", project, new_data)
    
    ui.navigate.to("/")

def page() -> None:
    dict_r = create_dict_counter_background("Background Noise Sensor R", "Voltage (mv)", [])
    dict_s = create_dict_counter_background("Background Noise Sensor S", "Voltage (mv)", [])
    dict_t = create_dict_counter_background("Background Noise Sensor T", "Voltage (mv)", [])
    
    dict_temp = tinydb_read("temp")[0]
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
                        on_click= lambda: stop_and_save(stop_event, [chart_r, chart_s, chart_s], dict_temp["name"])
                    )

    asyncio.create_task(update_appearance([chart_r, chart_s, chart_t], stop_event, run_event))