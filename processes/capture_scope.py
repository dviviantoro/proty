import os, sys
import time
import numpy as np
from multiprocessing import shared_memory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from modules.dsp import *
from modules.database import tinydb_update_temp

def parser_init():
    parser = argparse.ArgumentParser(description="Scope task")
    parser.add_argument(
        "-t",
        "--task",
        help="Scope task"
    )
    parser.add_argument(
        "-a",
        "--max",
        help="Max noise for filtering",
        default=None
    )
    parser.add_argument(
        "-i",
        "--min",
        help="Min noise for filtering",
        default=None
    )
    return parser

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
    pid_process = run_process("block")
    tinydb_update_temp("pid_capture", os.getpid())
    tinydb_update_temp("pid_scope", pid_process)

    while True:
        if flag_array[0]:
            # print(flag_array[0])
            # try:
            compile_resScope(
                process=args.task,
                dict_data=scope_array.copy(),
                max_filter=args.max,
                min_filter=args.min
            )
            flag_array[0] = 0
            # except Exception as e:
            #     print(e)
        else:
            time.sleep(1)