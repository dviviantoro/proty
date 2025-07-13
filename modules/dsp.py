import os, sys, lmdb
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.database import LMDBDict

def generate_sine(amplitude, phase_shift):
    x_axis = np.linspace(0, 360, 360, endpoint=False)
    y_axis = amplitude * np.sin(np.radians(x_axis + phase_shift))
    return np.column_stack((x_axis, y_axis))

def align_degree(data, n_wave):
    n_row = len(data)
    row_per_cycle = n_row / n_wave
    deg_per_row = 360 / row_per_cycle

    index_max = np.argmax(data[:int(row_per_cycle)])
    indices = np.arange(n_row)
    relative_indices = indices - index_max
    aligned_degrees = (90 + relative_indices * deg_per_row) % 360
    return aligned_degrees

def filter_noise(data, max, min):
    filtered_data = np.where((data > min) & (data < max), np.nan, data)
    return filtered_data

def filter_noise_and_align(source, sensor, max_filter, min_filter, cycle):
    sensor = sensor * 1000
    filtered_sensor = filter_noise(sensor, max_filter, min_filter)
    aligned_degree = align_degree(source, cycle)
    data_sensor = np.column_stack((aligned_degree, filtered_sensor))
    return data_sensor[~np.isnan(data_sensor).any(axis=1)]

def compile_resScope(process, dict_data, max_filter = 0, min_filter = 0):
    results = {}
    results["flag"] = True
    if process == "bgn":
        for i in range(2, 5):
            results[f"ch{i}"] = {}
            results[f"ch{i}"]["max"] = float(dict_data[f"ch{i}"].max())
            results[f"ch{i}"]["min"] = float(dict_data[f"ch{i}"].min())
    elif process == "cal":
        for i in range(2, 5):
            results[f"ch{i}"] = float(filter_noise(dict_data[f"ch{i}"], max_filter, min_filter).max())
    elif process == "aqc":
        data_source = dict_data["ch1"]
        for i in range(2, 5):
            data_sensor = filter_noise_and_align(data_source, dict_data[f"ch{i}"], max_filter, min_filter)
            data_sensor_pos = data_sensor[data_sensor[:, 1] > 0]
            data_sensor_neg = data_sensor[data_sensor[:, 1] < 0]
            
            results[f"ch{i}"] = {}
            results[f"ch{i}"]["posMax"] = np.max(data_sensor_pos[:, 1])
            results[f"ch{i}"]["posMin"] = np.min(data_sensor_pos[:, 1])
            results[f"ch{i}"]["posAvg"] = np.mean(data_sensor_pos[:, 1])
            results[f"ch{i}"]["posCnt"] = data_sensor_pos.shape[0]
            results[f"ch{i}"]["negMax"] = np.min(data_sensor_neg[:, 1])
            results[f"ch{i}"]["negMin"] = np.max(data_sensor_neg[:, 1])
            results[f"ch{i}"]["negAvg"] = np.mean(data_sensor_neg[:, 1])
            results[f"ch{i}"]["negCnt"] = data_sensor_neg.shape[0]

    with LMDBDict() as db:
        db.put(process, results)

    return results