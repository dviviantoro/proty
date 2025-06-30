import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
from data_buffer import data_buffer

# Global handle and config
chandle = ctypes.c_int16()
status = {}
buffer_size = 500  # Number of samples per fetch
channel_range = ps.PS2000A_RANGE['PS2000A_2V']

# Initialize and configure the PicoScope
def initialize_scope():
    # Open device
    status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
    assert_pico_ok(status["openunit"])

    # Enable Channel A (you can enable B the same way if needed)
    status["setChA"] = ps.ps2000aSetChannel(
        chandle,
        ps.PS2000A_CHANNEL["PS2000A_CHANNEL_A"],
        1,  # Enable
        ps.PS2000A_COUPLING["PS2000A_DC"],
        channel_range,
        0.0,
    )
    assert_pico_ok(status["setChA"])

    # Set data buffer
    global bufferAMax
    bufferAMax = np.zeros(shape=buffer_size, dtype=np.int16)

    status["setDataBuffers"] = ps.ps2000aSetDataBuffers(
        chandle,
        ps.PS2000A_CHANNEL["PS2000A_CHANNEL_A"],
        bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
        None,
        buffer_size,
        0,
        ps.PS2000A_RATIO_MODE["PS2000A_RATIO_MODE_NONE"],
    )
    assert_pico_ok(status["setDataBuffers"])

    # Set streaming parameters
    sample_interval = ctypes.c_int32(1000)  # 1 ms = 1000 µs
    status["runStreaming"] = ps.ps2000aRunStreaming(
        chandle,
        ctypes.byref(sample_interval),
        ps.PS2000A_TIME_UNITS["PS2000A_US"],
        0,
        buffer_size,
        1,  # autoStop
        1,
        ps.PS2000A_RATIO_MODE["PS2000A_RATIO_MODE_NONE"],
        buffer_size,
    )
    assert_pico_ok(status["runStreaming"])

    print("PicoScope initialized and streaming...")

# Fetch the latest buffer and update shared data
def get_latest_data():
    # Poll the device
    ps.ps2000aGetStreamingLatestValues(chandle, None, None)

    # Copy from bufferAMax to the shared buffer (just simulate some new data)
    time_axis = np.linspace(0, (buffer_size - 1), buffer_size)

    # Get max ADC value
    maxADC = ctypes.c_int16()
    ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
    mv_values = adc2mV(bufferAMax, channel_range, maxADC)

    # Update the shared buffer
    data_buffer["x_data"] = time_axis.tolist()
    data_buffer["y_data"] = mv_values.tolist()

# Optionally: clean up the scope
def stop_and_close():
    ps.ps2000aStop(chandle)
    ps.ps2000aCloseUnit(chandle)
