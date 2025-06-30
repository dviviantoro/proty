import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import define_shared_data, define_shared_flag

while True:
    shared_flag = define_shared_flag(False, "flag")
    # if shared_flag[1] == 1:
        # data_time = np.arange(0, len(data_sensor))
        # data_sensor = shared_data.copy()
        # chart.options['series'][0]['data'] = np.column_stack((data_time, data_sensor))
        # chart.update()
        
    # print(shared_flag)
    print("shared_flag")
    print(shared_flag)
    time.sleep(1)
