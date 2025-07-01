import time
import numpy as np
from multiprocessing import shared_memory

flag_data = np.zeros(2, dtype=np.int32)
flag_shm = shared_memory.SharedMemory(create=True, size=flag_data.nbytes, name='flag')
flag_array = np.ndarray(flag_data.shape, dtype=flag_data.dtype, buffer=flag_shm.buf)

scope_shm = {}
scope_array = {}
scope_data = np.zeros(416000, dtype=np.float64)
for i in range(1, 5):
    scope_shm[f"ch{i}"] = shared_memory.SharedMemory(create=True, size=scope_data.nbytes, name=f'ch{i}')
    scope_array[f"ch{i}"] = np.ndarray(scope_data.shape, dtype=scope_data.dtype, buffer=scope_shm[f"ch{i}"].buf)

try:
    print("Reader is running...")
    while True:
        if flag_array[1]:
            print(flag_array[0])
            print(flag_array[1])

            flag_array[1] = 0  # reset flag
        else:
            time.sleep(0.001)

except KeyboardInterrupt:
    pass
finally:
    flag_shm.close()
    scope_shm.close()