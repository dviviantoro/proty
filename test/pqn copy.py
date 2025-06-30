import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dsp import aligning_degree, filtering_noise, creating_dummy_y

def create_dummy_data(path):
    df = pd.read_csv(path, header=None, usecols=[3, 4], names=['Time', 'Vol'])
    df = df.dropna()
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    df['Vol'] = pd.to_numeric(df['Vol'], errors='coerce')
    df = df.dropna()
    # print(df)

    time_array = df['Time'].to_numpy()
    vol_array = df['Vol'].to_numpy()
    return time_array, vol_array

def test_multi_plot(*data_series):
    print("Start plotting")
    
    plt.figure(figsize=(10, 5))
    
    for x_axis, y_axis, label, color in data_series:
        plt.scatter(x_axis, y_axis, label=label, color=color)
    
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title('Time vs Voltage')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def getting_phase(data, aligned_data):
    pos_indices = np.where(~np.isnan(data) & (data > 0))[0]
    pos_occurance_deg = aligned_data[pos_indices]

    pos_mask_bot = pos_occurance_deg > 270
    pos_mask_top = pos_occurance_deg < 270

    neg_indices = np.where(~np.isnan(data) & (data < 0))[0]
    neg_occurance_deg = aligned_data[neg_indices]

    dict_phase = {}
    if np.any(pos_mask_bot):
        dict_phase["pos"] = {
            "bot": float(np.min(pos_occurance_deg[pos_mask_bot])),
            "top": float(np.max(pos_occurance_deg[pos_mask_top])),
        }
    else:
        dict_phase["pos"] = {
        "bot": float(np.min(pos_occurance_deg[pos_mask_top])),
        "top": float(np.max(pos_occurance_deg[pos_mask_top])),
    }
    dict_phase["neg"] = {
        "bot": float(np.min(neg_occurance_deg)),
        "top": float(np.max(neg_occurance_deg)),
    }

    print(dict_phase)
    return dict_phase

def getting_charge(data):
    pos_val = data[data > 0]
    pos_avg = np.nanmean(pos_val)
    pos_max_val = np.nanmax(pos_val)
    pos_min_val = np.nanmin(pos_val)

    neg_val = data[data < 0]
    neg_avg = np.nanmean(neg_val)
    neg_min_val = np.nanmax(neg_val)
    neg_max_val = np.nanmin(neg_val)
    
    dict_charge = {
        "pos": {
            "avg": float(pos_avg),
            "max": float(pos_max_val),
            "min": float(pos_min_val)
        },
        "neg": {
            "avg": float(neg_avg),
            "max": float(neg_max_val),
            "min": float(neg_min_val)
        }
    }

    print(dict_charge)
    return dict_charge

def getting_n(data):
    pos_count = np.sum(data > 0)
    neg_count = np.sum(data < 0)
    
    dict_count = {
        "pos": int(pos_count),
        "neg": int(neg_count)
    }

    print(dict_count)
    return pos_count, neg_count



time_source, vol_source = create_dummy_data("/Users/deny/proty02/assets/csv/sample2/pfugsumber.csv")
time_sensor, vol_sensor = create_dummy_data("/Users/deny/proty02/assets/csv/sample2/pfugrc.csv")
fitered_vol_sensor = filtering_noise(vol_sensor, 0.0048, -0.0045)

aligned_degree = aligning_degree(vol_source, 3.5)
new_y = creating_dummy_y(aligned_degree, 0.01)

getting_n(fitered_vol_sensor)
getting_charge(fitered_vol_sensor)
getting_phase(fitered_vol_sensor, aligned_degree)

test_multi_plot(
    (aligned_degree, new_y, 'source', 'blue'),
    (aligned_degree, fitered_vol_sensor, 'sensor', 'red'),
)



"""
pqn
phase
muatan
n pd
"""