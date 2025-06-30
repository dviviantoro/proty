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
channel_range = 7

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
status["setChB"] = ps.ps2000aSetChannel(chandle,
                                        ps.PS2000A_CHANNEL['PS2000A_CHANNEL_B'],
                                        enabled,
                                        ps.PS2000A_COUPLING['PS2000A_DC'],
                                        ps.PS2000A_RANGE['PS2000A_2V'],
                                        analogue_offset)
assert_pico_ok(status["setChB"])
status["setChC"] = ps.ps2000aSetChannel(chandle,
                                        ps.PS2000A_CHANNEL['PS2000A_CHANNEL_C'],
                                        enabled,
                                        ps.PS2000A_COUPLING['PS2000A_DC'],
                                        ps.PS2000A_RANGE['PS2000A_2V'],
                                        analogue_offset)
assert_pico_ok(status["setChC"])
status["setChD"] = ps.ps2000aSetChannel(chandle,
                                        ps.PS2000A_CHANNEL['PS2000A_CHANNEL_D'],
                                        enabled,
                                        ps.PS2000A_COUPLING['PS2000A_DC'],
                                        ps.PS2000A_RANGE['PS2000A_2V'],
                                        analogue_offset)
assert_pico_ok(status["setChC"])
print(status)

sizeOfOneBuffer = 250000
numBuffersToCapture = 1
totalSamples = sizeOfOneBuffer * numBuffersToCapture
bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
bufferBMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
bufferCMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
bufferDMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
memory_segment = 0
status["setDataBuffersA"] = ps.ps2000aSetDataBuffers(chandle,
                                                     ps.PS2000A_CHANNEL['PS2000A_CHANNEL_A'],
                                                     bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersA"])
status["setDataBuffersB"] = ps.ps2000aSetDataBuffers(chandle,
                                                     ps.PS2000A_CHANNEL['PS2000A_CHANNEL_B'],
                                                     bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersB"])
status["setDataBuffersC"] = ps.ps2000aSetDataBuffers(chandle,
                                                     ps.PS2000A_CHANNEL['PS2000A_CHANNEL_C'],
                                                     bufferCMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersC"])
status["setDataBuffersD"] = ps.ps2000aSetDataBuffers(chandle,
                                                     ps.PS2000A_CHANNEL['PS2000A_CHANNEL_D'],
                                                     bufferDMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersD"])
print(status)

# Begin streaming mode:
# sampleInterval = ctypes.c_int32(250)
sampleInterval = ctypes.c_int32(10)
sampleUnits = ps.PS2000A_TIME_UNITS['PS2000A_US']
maxPreTriggerSamples = 0
autoStopOn = 1
downsampleRatio = 1

def run_streaming():
    status["runStreaming"] = ps.ps2000aRunStreaming(chandle,
                                                    ctypes.byref(sampleInterval),
                                                    sampleUnits,
                                                    maxPreTriggerSamples,
                                                    totalSamples,
                                                    autoStopOn,
                                                    downsampleRatio,
                                                    ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'],
                                                    sizeOfOneBuffer)
    assert_pico_ok(status["runStreaming"])
    print(status)

run_streaming()

def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
    global nextSample, autoStopOuter, wasCalledBack
    wasCalledBack = True
    destEnd = nextSample + noOfSamples
    sourceEnd = startIndex + noOfSamples
    bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
    bufferCompleteB[nextSample:destEnd] = bufferBMax[startIndex:sourceEnd]
    bufferCompleteC[nextSample:destEnd] = bufferCMax[startIndex:sourceEnd]
    bufferCompleteD[nextSample:destEnd] = bufferDMax[startIndex:sourceEnd]
    nextSample += noOfSamples
    if autoStop:
        autoStopOuter = True

actualSampleInterval = sampleInterval.value
actualSampleIntervalNs = actualSampleInterval * 1000

print("Capturing at sample interval %s ns" % actualSampleIntervalNs)

def show_plotly(y):
    time = np.arange(0, len(y))
    fig = px.scatter(x=time, y=y)
    fig.show()

n = 0
meta = np.zeros(2, dtype=np.int32)
meta_shm = shared_memory.SharedMemory(create=True, size=meta.nbytes, name='flag')
meta_array = np.ndarray(meta.shape, dtype=meta.dtype, buffer=meta_shm.buf)

while True:
    n += 1
    try:
        bufferCompleteA = np.zeros(shape=totalSamples, dtype=np.int16)
        bufferCompleteB = np.zeros(shape=totalSamples, dtype=np.int16)
        bufferCompleteC = np.zeros(shape=totalSamples, dtype=np.int16)
        bufferCompleteD = np.zeros(shape=totalSamples, dtype=np.int16)
        nextSample = 0
        autoStopOuter = False
        wasCalledBack = False

        cFuncPtr = ps.StreamingReadyType(streaming_callback)
        while nextSample < totalSamples and not autoStopOuter:
            wasCalledBack = False
            ps.ps2000aGetStreamingLatestValues(chandle, cFuncPtr, None)
            if not wasCalledBack:
                time.sleep(0.01)

            # print(f"{nextSample} dan {totalSamples}")

        print("Done grabbing values.")
        maxADC = ctypes.c_int16()
        status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
        assert_pico_ok(status["maximumValue"])

        # Convert ADC counts data to mV
        adc2mVChAMax = np.array(adc2mV(bufferCompleteA, channel_range, maxADC))
        adc2mVChBMax = np.array(adc2mV(bufferCompleteB, channel_range, maxADC))
        adc2mVChCMax = np.array(adc2mV(bufferCompleteC, channel_range, maxADC))
        adc2mVChDMax = np.array(adc2mV(bufferCompleteD, channel_range, maxADC))
        
        if n == 1:
            shm = shared_memory.SharedMemory(create=True, size=adc2mVChAMax.nbytes, name='data')
            shared_array = np.ndarray(adc2mVChAMax.shape, dtype=adc2mVChAMax.dtype, buffer=shm.buf)
        
        shared_array[:] = adc2mVChAMax
        meta_array[0] = len(adc2mVChAMax)
        meta_array[1] = 1
        
        show_plotly(adc2mVChAMax)
        run_streaming()
    except KeyboardInterrupt:
        print("\nStopped by user.")

        status["stop"] = ps.ps2000aStop(chandle)
        assert_pico_ok(status["stop"])


        status["close"] = ps.ps2000aCloseUnit(chandle)
        assert_pico_ok(status["close"])