# reader.py
import numpy as np
from multiprocessing import shared_memory
import time

meta_shm = shared_memory.SharedMemory(name='flag')
meta_array = np.ndarray((2,), dtype=np.int32, buffer=meta_shm.buf)

existing_shm = shared_memory.SharedMemory(name='ch4')
shared_array = np.ndarray((416000,), dtype=np.float64, buffer=existing_shm.buf)

try:
    while True:
        if meta_array[1] == 1:
            data_copy = shared_array.copy()
            print(len(data_copy))
            print(data_copy)
            # print(data_copy.tolist())

            meta_array[1] = 0  # reset flag
        else:
            time.sleep(0.001)

except KeyboardInterrupt:
    pass
finally:
    existing_shm.close()
