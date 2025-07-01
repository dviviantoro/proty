import time
import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
from multiprocessing import shared_memory
import argparse

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

def ps_stop_unit():
    status["stop"] = ps.ps2000aStop(chandle)
    assert_pico_ok(status["stop"])
    status["close"] = ps.ps2000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

def ps_open_unit():
    status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
    assert_pico_ok(status["openunit"])
    print(status)

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

if __name__ == "__main__":
    args = parser_init().parse_args()

    ps_open_unit()
    ps_set_channel()
    ps_set_trigger()
    ps_get_timebase2()
    ps_create_buffer()

    flag_shm = shared_memory.SharedMemory(name='flag')
    flag_array = np.ndarray((2,), dtype=np.int32, buffer=flag_shm.buf)
    
    scope_shm = {}
    scope_array = {}
    for i in range(1, 5):
        scope_shm[f"ch{i}"] = shared_memory.SharedMemory(name=f'ch{i}')
        scope_array[f"ch{i}"] = np.ndarray((416000,), dtype=np.float64, buffer=scope_shm[f"ch{i}"].buf)
    
    while True:
        start_time = time.perf_counter()
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
            for i in range(1, 5):    
                dict_adc2mV[f"ch{i}"] = np.array(adc2mV(dict_buffer[f"bufferMax{i}"], chARange, maxADC))
                scope_array[f"ch{i}"][:] = dict_adc2mV[f"ch{i}"]

            if args.task == "bgn":
                flag_array[1] = 1
            elif args.task == "cal":
                flag_array[1] = 2
            elif args.task == "aqc":
                flag_array[1] = 3

            end_time = time.perf_counter()
            duration = end_time - start_time
            print(f"Loop took {duration:.6f} seconds")
        except KeyboardInterrupt:
            print("\nStopped by user.")
            ps_stop_unit()