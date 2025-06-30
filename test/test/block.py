import os
import time
import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
from multiprocessing import shared_memory
import subprocess
import plotly.express as px
import argparse
from dotenv import load_dotenv
load_dotenv()

cwd = os.getenv("CWD")

status = {}
dict_buffer = {}
enabled = 1
disabled = 0
analogue_offset = 0.0
chandle = ctypes.c_int16()
chARange = 7
channel_name = [1,2,3,4]

preTriggerSamples = 208000*1
postTriggerSamples = 208000*1
totalSamples = preTriggerSamples + postTriggerSamples

timebase = 8
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(0)

def parser_init():
    parser = argparse.ArgumentParser(description="Process the entry analogue data")
    parser.add_argument(
        "-t",
        "--task",
        help="What do you want? DSP for calibration, noise background, or continuous acquisition?"
    )
    return parser

def show_plotly(y):
    time = np.arange(0, len(y))
    fig = px.scatter(x=time, y=y)
    fig.show()

def ps_stop_unit():
    status["stop"] = ps.ps2000aStop(chandle)
    assert_pico_ok(status["stop"])
    status["close"] = ps.ps2000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

def ps_open_unit():
    status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
    assert_pico_ok(status["openunit"])

def ps_set_channel():
    for i in channel_name:
        set_channel = f"setCh{i}"
        status[set_channel] = ps.ps2000aSetChannel(chandle,
                                                i-1,
                                                enabled,
                                                ps.PS2000A_COUPLING['PS2000A_AC'],
                                                ps.PS2000A_RANGE['PS2000A_2V'],
                                                analogue_offset)
        assert_pico_ok(status[set_channel])
    print(status)

def ps_set_trigger():
    status["trigger"] = ps.ps2000aSetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 1000)
    assert_pico_ok(status["trigger"])
    print(status)

def ps_get_timebase2():
    status["getTimebase2"] = ps.ps2000aGetTimebase2(chandle,
                                                    timebase,
                                                    totalSamples,
                                                    ctypes.byref(timeIntervalns),
                                                    oversample,
                                                    ctypes.byref(returnedMaxSamples),
                                                    0)
    assert_pico_ok(status["getTimebase2"])
    print(status)

def ps_create_buffer():
    for i in channel_name:
        dict_buffer[f"bufferMax{i}"] = (ctypes.c_int16 * totalSamples)()
        dict_buffer[f"bufferMin{i}"] = (ctypes.c_int16 * totalSamples)()
        
        set_buffer = f"setDataBuffers{i}"
        status[set_buffer] = ps.ps2000aSetDataBuffers(chandle,
                                                            i-1,
                                                            ctypes.byref(dict_buffer[f"bufferMax{i}"]),
                                                            ctypes.byref(dict_buffer[f"bufferMin{i}"]),
                                                            totalSamples,
                                                            0,
                                                            0)
        assert_pico_ok(status[set_buffer])
        print(status)

def ps_run_block():
    status["runBlock"] = ps.ps2000aRunBlock(chandle,
                                                    preTriggerSamples,
                                                    postTriggerSamples,
                                                    timebase,
                                                    oversample,
                                                    None,
                                                    0,
                                                    None,
                                                    None)
    assert_pico_ok(status["runBlock"])
    print(status)

def ps_getValues():
    status["getValues"] = ps.ps2000aGetValues(chandle, 0, ctypes.byref(cTotalSamples), 0, 0, 0, ctypes.byref(overflow))
    assert_pico_ok(status["getValues"])

def ps_maximumValue():
    status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maximumValue"])
    
# def create_shared_flag():
#     meta = np.zeros(2, dtype=np.int32)
#     meta_shm = shared_memory.SharedMemory(create=True, size=meta.nbytes, name='flag')
#     meta_array = np.ndarray(meta.shape, dtype=meta.dtype, buffer=meta_shm.buf)
#     return meta_array

# def create_shared_data(data):
#     shm = shared_memory.SharedMemory(create=True, size=data.nbytes, name='data')
#     shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
#     return shared_array

def do_dsp(task):
    command = [
        f"{cwd}/.venv/Scripts/python.exe",
        f"{cwd}/signaling/dsp.py",
        "-t", task
    ]
    print(command)
    subprocess.Popen(command)

if __name__ == "__main__":
    """
    meta index:
    1. 0: close scope, 1: start scope
    2. 0: data not ready, 1: data ready
    """

    args = parser_init().parse_args()
    

    ps_open_unit()
    ps_set_channel()
    ps_set_trigger()
    ps_get_timebase2()
    ps_create_buffer()

    meta = np.zeros(2, dtype=np.int32)
    meta_shm = shared_memory.SharedMemory(create=True, size=meta.nbytes, name='flag')
    shared_flag = np.ndarray(meta.shape, dtype=meta.dtype, buffer=meta_shm.buf)

    n = 0
    while True:
        start_time = time.perf_counter()
        n += 1
        try:
            ps_run_block()

            ready = ctypes.c_int16(0)
            check = ctypes.c_int16(0)
            while ready.value == check.value:
                status["isReady"] = ps.ps2000aIsReady(chandle, ctypes.byref(ready))

            overflow = ctypes.c_int16()
            cTotalSamples = ctypes.c_int32(totalSamples)
            ps_getValues()
            maxADC = ctypes.c_int16()
            ps_maximumValue()

            dict_adc2mV = {}
            for i in channel_name:    
                dict_adc2mV[f"ch{i}"] = np.array(adc2mV(dict_buffer[f"bufferMax{i}"], chARange, maxADC))

            if n == 1:
                dict_shm = {}
                dict_shared_data = {}
                for i in channel_name:
                    data_name = f'ch{i}'
                    dict_shm[data_name] = shared_memory.SharedMemory(create=True, size=dict_adc2mV[data_name].nbytes, name=data_name)
                    dict_shared_data[data_name] = np.ndarray(dict_adc2mV[data_name].shape, dtype=dict_adc2mV[data_name].dtype, buffer=dict_shm[data_name].buf)
                    print(dict_adc2mV[data_name].shape)
                    print(dict_adc2mV[data_name].dtype)
                    

            """
            """
            for i in channel_name:
                dict_shared_data[f"ch{i}"][:] = dict_adc2mV[f"ch{i}"] 
                print(dict_shared_data[f"ch{i}"])
                # print(f"data shared: ch{i}")
                # show_plotly(dict_adc2mV[f"ch{i}"])

            shared_flag[1] = 1
            do_dsp(args.task)
            time.sleep(20)

            end_time = time.perf_counter()  # End timing
            duration = end_time - start_time
            print(f"Loop {n} took {duration:.6f} seconds")

        except KeyboardInterrupt:
            print("\nStopped by user.")
            status["stop"] = ps.ps2000aStop(chandle)
            assert_pico_ok(status["stop"])
            status["close"] = ps.ps2000aCloseUnit(chandle)
            assert_pico_ok(status["close"])