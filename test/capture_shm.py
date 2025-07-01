# reader.py
import numpy as np
from multiprocessing import shared_memory
import time
import plotly.express as px

flag_data = np.zeros(2, dtype=np.int32)
flag_shm = shared_memory.SharedMemory(create=True, size=flag_data.nbytes, name='flag')
flag_array = np.ndarray(flag_data.shape, dtype=flag_data.dtype, buffer=flag_shm.buf)

scope_shm = {}
scope_array = {}
scope_data = np.zeros(416000, dtype=np.float64)
for i in range(1, 5):
    scope_shm[f"ch{i}"] = shared_memory.SharedMemory(create=True, size=scope_data.nbytes, name=f'ch{i}')
    scope_array[f"ch{i}"] = np.ndarray(scope_data.shape, dtype=scope_data.dtype, buffer=scope_shm[f"ch{i}"].buf)

# meta_shm = shared_memory.SharedMemory(name='flag')
# meta_array = np.ndarray((2,), dtype=np.int32, buffer=meta_shm.buf)

# existing_shm = shared_memory.SharedMemory(name='ch4')
# shared_array = np.ndarray((416000,), dtype=np.float64, buffer=existing_shm.buf)

def show_plotly(y):
    time = np.arange(0, len(y))
    fig = px.scatter(x=time, y=y)
    fig.show()

try:
    print("Reader is running...")
    while True:
        if flag_array[1]:
            print(flag_array[0])
            print(flag_array[1])

            # print(scope_array[f"ch1"])
            # show_plotly(scope_array[f"ch1"])
            show_plotly(scope_array[f"ch2"])
            # data_copy = shared_array.copy()
            # print(len(data_copy))
            # print(data_copy)
            # print(data_copy.tolist())

            flag_array[1] = 0  # reset flag
        else:
            time.sleep(0.001)

except KeyboardInterrupt:
    pass
# finally:
#     existing_shm.close()