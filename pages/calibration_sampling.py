import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from pages.theme import frame
from modules.dictionary import *
from modules.database import tinydb_read, tinydb_append_xy
from modules.template_ui import ToggleButtonAsync, grid_content_calibration, update_grid_content_calibration

from modules.dsp import *
import asyncio
import random

async def update_appearance(charge, charts, grids, codes, dict_temp, stop_event, run_event):
    try:
        while not stop_event.is_set():
            await run_event.wait()
            random_pos = random.randint(1, 10)
            for i in range(0, 3):
                charts[i].options['dataset']['source'].append([random_pos, int(charge.value)])
                charts[i].update()

                xy = charts[i].options['dataset']['source']
                x = [point[0] for point in xy]
                y = [point[1] for point in xy]
                update_grid_content_calibration(grids[i], x, y)
                
                codes[i].set_content(general_data_sentence(dict_temp, keys_calibration, len(x)))

                # linear equation
                slope, intercept = np.polyfit(x, y, 1)
                trendline_x = np.array([min(x), max(x)])
                trendline_y = slope * trendline_x + intercept
                trendline_data = list(zip(trendline_x, trendline_y)) #ready for echart

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Update task cancelled.")
    finally:
        print("Update task finished.")

async def delete_rows(grid, chart, code, dict_temp):
    rows = await grid.get_selected_rows()
    if rows:
        for row in rows:
            xy = chart.options['dataset']['source']
            target = [row['voltage'], row['charge']]
            xy.remove(target)
            chart.options['dataset']['source'] = xy
            chart.update()

            x = [point[0] for point in xy]
            y = [point[1] for point in xy]
            update_grid_content_calibration(grid, x, y)

            code.set_content(general_data_sentence(dict_temp, len(x)))
    else:
        ui.notify('No rows selected.')

def stop_and_save(stop_event, charts, project):
    stop_event.set()
    for chart in charts:
        tinydb_append_xy("calibration", project, chart.options['dataset']['source'])
    ui.navigate.to("/")

def page() -> None:
    dict_r = create_dict_calibration("Calibration Sensor Phase R", [])
    dict_s = create_dict_calibration("Calibration Sensor Phase S", [])
    dict_t = create_dict_calibration("Calibration Sensor Phase T", [])
    dict_temp = tinydb_read("temp")[0]
    stop_event = asyncio.Event()
    run_event = asyncio.Event()
    run_event.clear()

    with frame("Oscilloscope Panel", "OK!"):
        with ui.tabs().classes('w-full') as tabs:
            tab_r = ui.tab('Phase R')
            tab_s = ui.tab('Phase S')
            tab_t = ui.tab('Phase T')
        with ui.tab_panels(tabs, value=tab_r).classes('w-full'):
            with ui.tab_panel(tab_r):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-10 mb-10'):
                    chart_r = ui.echart(options=dict_r).classes('h-[640px] col-start-1 col-span-8 size-full')
                    with ui.card().classes('col-start-9 col-span-4 size-full'):
                        ui.label('[Background Noise] My title is')
                        code_r = ui.code(general_data_sentence(dict_temp, keys_calibration, 0)).classes('w-full')
                        grid_r = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        with ui.row().classes("w-full place-content-center"):
                            ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_r, chart_r, code_r, dict_temp))
            with ui.tab_panel(tab_s):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-10 mb-10'):
                    chart_s = ui.echart(options=dict_s).classes('h-[640px] col-start-1 col-span-8 size-full')
                    with ui.card().classes('col-start-9 col-span-4 size-full'):
                        ui.label('[Background Noise] My title is')
                        code_s = ui.code(general_data_sentence(dict_temp, keys_calibration, 0)).classes('w-full')
                        grid_s = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        with ui.row().classes("w-full place-content-center"):
                            ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_s, chart_s, code_s, dict_temp))
            with ui.tab_panel(tab_t):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-10 mb-10'):
                    chart_t = ui.echart(options=dict_t).classes('h-[640px] col-start-1 col-span-8 size-full')
                    with ui.card().classes('col-start-9 col-span-4 size-full'):
                        ui.label('[Background Noise] My title is')
                        code_t = ui.code(general_data_sentence(dict_temp, keys_calibration, 0)).classes('w-full')
                        grid_t = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        with ui.row().classes("w-full place-content-center"):
                            ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_t, chart_t, code_t, dict_temp))
        with ui.page_sticky(x_offset=18, y_offset=18, position="bottom").classes("w-full place-content-center"):
            with ui.row().classes("w-full place-content-center"):
                charge = ui.number(label="Charge in pC")
            ToggleButtonAsync(run_event)
            ui.button(
                "Stop and Save",
                icon="stop_circle",
                color="red",
                on_click= lambda: stop_and_save(stop_event, [chart_r, chart_s, chart_s], dict_temp["name"])
            )
    asyncio.create_task(
        update_appearance(
            charge,
            [chart_r, chart_s, chart_t],
            [grid_r, grid_s, grid_t],
            [code_r, code_s, code_t],
            dict_temp,
            stop_event,
            run_event
        )
    )