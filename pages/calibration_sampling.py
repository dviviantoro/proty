import os, sys, signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from pages.theme import frame
from modules.dictionary import *
from modules.database import tinydb_read, tinydb_append_xy, LMDBDict
from modules.template_ui import ToggleButtonAsync, grid_content_calibration, update_grid_content_calibration
from modules.dsp import create_lineq
import asyncio

async def update_appearance(stop_event, run_event, charts, summaries, grids, dict_temp, charge):
    try:
        while not stop_event.is_set():
            await run_event.wait()

            with LMDBDict() as db:
                retrieved_data = db.get("cal")
                if retrieved_data["flag"]:
                    print("updating calibration page")
                    channels = ["ch2", "ch3", "ch4"]

                    for i in range(0,3):
                        general_data = generate_string_general("general", dict_temp, keys_background)
                        charts[i].options['dataset']['source'].append([retrieved_data[channels[i]], int(charge.value)])
                        charts[i].update()

                        x = [point[0] for point in charts[i].options['dataset']['source']]
                        y = [point[1] for point in charts[i].options['dataset']['source']]
                        update_grid_content_calibration(grids[i], x, y)

                        lineq = create_lineq(x, y)
                        if lineq:
                            cal_data = summary_cal(lineq, len(x))
                            general_data = general_data + cal_data
                        summaries[i].set_content(general_data)

                    retrieved_data["flag"] = False
                    db.put("cal", retrieved_data)

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Update task cancelled.")
    finally:
        print("Update task finished.")

async def delete_rows(grid, chart, summary, dict_temp):
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

            general_data = generate_string_general("general", dict_temp, keys_background)
            cal_data = summary_cal(x, y)
            full_summary = general_data + cal_data
            summary.set_content(full_summary)
    else:
        ui.notify('No rows selected.')

def stop_and_save(stop_event, charts, project):
    stop_event.set()

    dict_temp = tinydb_read("temp")[0]
    os.kill(dict_temp["pid_capture"], signal.SIGTERM)
    os.kill(dict_temp["pid_scope"], signal.SIGTERM)

    for chart in charts:
        tinydb_append_xy("calibration", project, chart.options['dataset']['source'])

    ui.navigate.to("/")

def page() -> None:
    run_process("capture_scope", ["-t", "cal", "-a", "0", "-i", "0"])

    app.storage.user['cal_charge'] = None

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
                        summary_r = ui.code(generate_string_general("general_data", dict_temp, keys_calibration)).classes('w-full')
                        grid_r = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        with ui.row().classes("w-full place-content-center"):
                            ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_r, chart_r, summary_r, dict_temp))
            with ui.tab_panel(tab_s):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-10 mb-10'):
                    chart_s = ui.echart(options=dict_s).classes('h-[640px] col-start-1 col-span-8 size-full')
                    with ui.card().classes('col-start-9 col-span-4 size-full'):
                        ui.label('[Background Noise] My title is')
                        summary_s = ui.code(generate_string_general("general_data", dict_temp, keys_calibration)).classes('w-full')
                        grid_s = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        with ui.row().classes("w-full place-content-center"):
                            ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_s, chart_s, summary_s, dict_temp))
            with ui.tab_panel(tab_t):
                with ui.element('div').classes('grid grid-cols-12 w-full gap-5 mt-10 mb-10'):
                    chart_t = ui.echart(options=dict_t).classes('h-[640px] col-start-1 col-span-8 size-full')
                    with ui.card().classes('col-start-9 col-span-4 size-full'):
                        ui.label('[Background Noise] My title is')
                        summary_t = ui.code(generate_string_general("general_data", dict_temp, keys_calibration)).classes('w-full')
                        grid_t = ui.aggrid(grid_content_calibration()).classes('h-[320px]')
                        with ui.row().classes("w-full place-content-center"):
                            ui.button("Delete row(s)", icon="delete", color="red", on_click= lambda: delete_rows(grid_t, chart_t, summary_t, dict_temp))
        with ui.page_sticky(x_offset=18, y_offset=18, position="bottom").classes("w-full place-content-center"):
            with ui.row().classes("w-full place-content-center"):
                charge = ui.number(label="Charge in pC").bind_value(app.storage.user, 'cal_charge')
            ToggleButtonAsync(run_event).bind_enabled_from(app.storage.user, 'cal_charge', lambda val: val is not None)
            ui.button(
                "Stop and Save",
                icon="stop_circle",
                color="red",
                on_click= lambda: stop_and_save(stop_event, [chart_r, chart_s, chart_s], dict_temp["name"])
            )

    asyncio.create_task(
        update_appearance(
            stop_event,
            run_event,
            [chart_r, chart_s, chart_t],
            [summary_r, summary_s, summary_t],
            [grid_r, grid_s, grid_t],
            dict_temp,
            charge,
        )
    )