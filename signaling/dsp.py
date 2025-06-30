import os
import time
import numpy as np
from multiprocessing import shared_memory
import subprocess
import argparse
from dotenv import load_dotenv
import plotly.express as px
load_dotenv()

cwd = os.getenv("CWD")

def parser_init():
    parser = argparse.ArgumentParser(description="Process the entry analogue data")
    parser.add_argument(
        "-t",
        "--task",
        help="What do you want? DSP for calibration, noise background, or continuous acquisition?"
    )
    return parser

def do_calibration():
    print("comething")
# def do_background
# def do_acquisition

def show_plotly(y):
    time = np.arange(0, len(y))
    fig = px.scatter(x=time, y=y)
    fig.show()

if __name__ == "__main__":
    time.sleep(1)
    args = parser_init().parse_args()

    flag_shm = shared_memory.SharedMemory(name='flag')
    flag_array = np.ndarray((2,), dtype=np.int32, buffer=flag_shm.buf)
        
    dict_shared_data = {}
    for i in range(1, 5):
        data_shm = shared_memory.SharedMemory(name=f"ch{i}")
        dict_shared_data[f"ch{i}"] = np.ndarray((208000*2,), dtype=np.float64, buffer=data_shm.buf)        
        accepted_data = dict_shared_data[f"ch{i}"].copy()
        # show_plotly(accepted_data)

    flag_array[1] = 0
    if args.task == "calibration":
        do_calibration()