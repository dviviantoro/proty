import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time
import plotly.express as px
from multiprocessing import shared_memory

status = {}
enabled = 1
disabled = 0
analogue_offset = 0.0
chandle = ctypes.c_int16()
chARange = 7
channel_name = ["A", "B", "C", "D"]

status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
assert_pico_ok(status["openunit"])
print(status)

status["setChA"] = ps.ps2000aSetChannel(chandle,
                                        ps.PS2000A_CHANNEL['PS2000A_CHANNEL_A'],
                                        enabled,
                                        ps.PS2000A_COUPLING['PS2000A_DC'],
                                        ps.PS2000A_RANGE['PS2000A_2V'],
                                        analogue_offset)
assert_pico_ok(status["setChA"])

status["trigger"] = ps.ps2000aSetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 1000)
assert_pico_ok(status["trigger"])

# preTriggerSamples = 207500
# postTriggerSamples = 207500
preTriggerSamples = 208000
postTriggerSamples = 208000
totalSamples = preTriggerSamples + postTriggerSamples

timebase = 8
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(0)
status["getTimebase2"] = ps.ps2000aGetTimebase2(chandle,
                                                timebase,
                                                totalSamples,
                                                ctypes.byref(timeIntervalns),
                                                oversample,
                                                ctypes.byref(returnedMaxSamples),
                                                0)
assert_pico_ok(status["getTimebase2"])

def show_plotly(y):
    time = np.arange(0, len(y))
    fig = px.scatter(x=time, y=y)
    fig.show()

def stop_unit():
    status["stop"] = ps.ps2000aStop(chandle)
    assert_pico_ok(status["stop"])
    status["close"] = ps.ps2000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

n = 0
meta = np.zeros(2, dtype=np.int32)
meta_shm = shared_memory.SharedMemory(create=True, size=meta.nbytes, name='flag')
meta_array = np.ndarray(meta.shape, dtype=meta.dtype, buffer=meta_shm.buf)

# Create buffers ready for assigning pointers for data collection

dict_buffer = {}
for i in channel_name:
    dict_buffer[f"buffer{i}max"] = (ctypes.c_int16 * totalSamples)()
    dict_buffer[f"buffer{i}min"] = (ctypes.c_int16 * totalSamples)()

# bufferAMax = (ctypes.c_int16 * totalSamples)()
# bufferAMin = (ctypes.c_int16 * totalSamples)()
# bufferBMax = (ctypes.c_int16 * totalSamples)()
# bufferBMin = (ctypes.c_int16 * totalSamples)()
# bufferCMax = (ctypes.c_int16 * totalSamples)()
# bufferCMin = (ctypes.c_int16 * totalSamples)()
# bufferDMax = (ctypes.c_int16 * totalSamples)()
# bufferDMin = (ctypes.c_int16 * totalSamples)()

status["setDataBuffersA"] = ps.ps2000aSetDataBuffers(chandle,
                                                    0,
                                                    ctypes.byref(bufferAMax),
                                                    ctypes.byref(bufferAMin),
                                                    totalSamples,
                                                    0,
                                                    0)
assert_pico_ok(status["setDataBuffersA"])

while True:
    n += 1
    try:
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

        ready = ctypes.c_int16(0)
        check = ctypes.c_int16(0)
        while ready.value == check.value:
            status["isReady"] = ps.ps2000aIsReady(chandle, ctypes.byref(ready))

        overflow = ctypes.c_int16()
        cTotalSamples = ctypes.c_int32(totalSamples)
        status["getValues"] = ps.ps2000aGetValues(chandle, 0, ctypes.byref(cTotalSamples), 0, 0, 0, ctypes.byref(overflow))
        assert_pico_ok(status["getValues"])

        maxADC = ctypes.c_int16()
        status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
        assert_pico_ok(status["maximumValue"])

        # convert ADC counts data to mV
        adc2mVChAMax =  np.array(adc2mV(bufferAMax, chARange, maxADC))

        if n == 1:
            shm = shared_memory.SharedMemory(create=True, size=adc2mVChAMax.nbytes, name='data')
            shared_array = np.ndarray(adc2mVChAMax.shape, dtype=adc2mVChAMax.dtype, buffer=shm.buf)
        
        show_plotly(adc2mVChAMax)
        shared_array[:] = adc2mVChAMax
        meta_array[0] = len(adc2mVChAMax)
        meta_array[1] = 1
        print(f"looping: {n}")
        time.sleep(10)

    except KeyboardInterrupt:
        print("\nStopped by user.")

        status["stop"] = ps.ps2000aStop(chandle)
        assert_pico_ok(status["stop"])


        status["close"] = ps.ps2000aCloseUnit(chandle)
        assert_pico_ok(status["close"])