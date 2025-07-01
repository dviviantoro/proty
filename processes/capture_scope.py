import os, sys
import time
import numpy as np
from multiprocessing import shared_memory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from modules.dsp import *

flag_data = np.zeros(1, dtype=np.int32)
flag_shm = shared_memory.SharedMemory(create=True, size=flag_data.nbytes, name='flag')
flag_array = np.ndarray(flag_data.shape, dtype=flag_data.dtype, buffer=flag_shm.buf)

scope_shm = {}
scope_array = {}
scope_data = np.zeros(416000, dtype=np.float64)
for i in range(1, 5):
    scope_shm[f"ch{i}"] = shared_memory.SharedMemory(create=True, size=scope_data.nbytes, name=f'ch{i}')
    scope_array[f"ch{i}"] = np.ndarray(scope_data.shape, dtype=scope_data.dtype, buffer=scope_shm[f"ch{i}"].buf)

if __name__ == "__main__":
    args = parser_init().parse_args()
    run_process("block")

    while True:
        if flag_array[0]:
            print(flag_array[0])
            compile_resScope(args.task, scope_array.copy(), args.max, args.min)
            flag_array[0] = 0
        else:
            time.sleep(1)