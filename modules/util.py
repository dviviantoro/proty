import os, io, sys
import logging
import shutil
import argparse
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import date, datetime, timedelta, timezone
from nicegui import app, ui
import numpy as np
load_dotenv()

cwd = Path.cwd()
home_dir = Path.home()
temp_dir = home_dir / ".proty"
base_db = cwd / "assets" / "app.json"

passwords = {'user1': 'pass1', 'user2': 'pass2'}
static_file = cwd / "assets"
lottie_player = cwd / "assets" / "lottie" / "player.js"
logo_img = cwd / "assets" / "logo_proty.png"

python_app = cwd / '.venv' / 'Scripts' / 'python.exe'

keys_background = ["timestamp", "operator", "name", "location", "sensor", "phase"]
keys_calibration = ["timestamp", "operator", "name", "location", "sensor", "phase", "calibrator", "background"]
keys_acquisition = ["timestamp", "operator", "name", "location", "sensor", "background", "calibration", "phase_ref"]
keys_prpd = ["count", "maxCharge", "minCharge", "avgCharge", "startDeg", "endDeg"]
keys_database = ["timestamp", "operator", "name", "location", "sensor", "phase"]

influx_host = os.getenv('INFLUX_HOST')
influx_token = os.getenv('INFLUX_TOKEN')
influx_database = os.getenv('INFLUX_DATABASE')

logging.basicConfig(
    level=logging.INFO,  # <--- Crucial: INFO level is enabled
    format='%(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()] # <--- Crucial: Sends to console (stderr)
)
logger = logging.getLogger(__name__)

ui.tab.default_props('no-caps')

def parser_init():
    parser = argparse.ArgumentParser(description="Scope task")
    parser.add_argument(
        "-t",
        "--task",
        help="Scope task"
    )
    parser.add_argument(
        "-a",
        "--max",
        help="Max noise for filtering",
        default=None
    )
    parser.add_argument(
        "-i",
        "--min",
        help="Min noise for filtering",
        default=None
    )
    return parser

def create_dir(directory_name):
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            shutil.copy(base_db, temp_dir)
            logger.info(f"Directory '{directory_name}' created successfully.")
        else:
            logger.warning(f"Directory '{directory_name}' already exists.")
    except OSError as error:
        logger.error(f"Error creating directory '{directory_name}': {error}")

create_dir(temp_dir)

def create_sentence(title, data, keys, point):
    data_items = []
    for key in keys:
        if key in data:
            value = data[key]
            if isinstance(value, str):
                data_items.append(f'    "{key}": "{value}"')
            elif value is None:
                data_items.append(f'    "{key}": None')
            else:
                data_items.append(f'    "{key}": {value}')
    if point: data_items.append(f'    "point": {point}')
    body = ",\n".join(data_items)
    sentence = f"""{title} = {{
{body}
}}
"""
    return sentence

def run_process(process, args=[]):
    python_path = cwd / "processes" / f"{process}.py"
    command = [python_app, python_path] + args
    process_obj = subprocess.Popen(command)
    return process_obj.pid

def create_summary_background(
        data,
        count,
        avg_r,
        max_r,
        min_r,
        avg_s,
        max_s,
        min_s,
        avg_t,
        max_t,
        min_t,
        ):
    created = data["timestamp"]
    operator = data["operator"]
    title = data["title"]
    location = data["location"]
    sensor = data["sensor"]

    sentence = f"""
    metadata = {{
        "created": {created},
        "title": {title},
        "operator": {operator},
        "location": {location},
        "sensor_id": {sensor},
        "sampling_count": {count},
        "data_sensor_r": {{
            "avg": {avg_r},
            "max": {max_r},
            "min": {min_r},
            "units": "mV"
        }},
        "data_sensor_s": {{
            "avg": {avg_s},
            "max": {max_s},
            "min": {min_s},
            "units": "mV"
        }},
        "data_sensor_t": {{
            "avg": {avg_t},
            "max": {max_t},
            "min": {min_t},
            "units": "mV"
        }},
    }}
"""
    return sentence