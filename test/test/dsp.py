import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# example
# num_rows = 87500
# num_waves = 3.5
# rows_per_cycle = num_rows / num_waves
# degrees_per_row = 360 / rows_per_cycle
# index_max = np.argmax(vol_array[:int(rows_per_cycle)])

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

def aligning_degree(data, n_wave):
    n_row = len(data)
    row_per_cycle = n_row / n_wave
    deg_per_row = 360 / row_per_cycle

    index_max = np.argmax(data[:int(row_per_cycle)])
    indices = np.arange(n_row)
    relative_indices = indices - index_max
    aligned_degrees = (90 + relative_indices * deg_per_row) % 360
    return aligned_degrees

def filtering_noise(data, max, min):
    filtered_data = np.where((data > min) & (data < max), np.nan, data)
    return filtered_data

def create_dummy_y(aligned_degrees, amplitude):
    radians = np.deg2rad(aligned_degrees)
    y_values = amplitude * np.sin(radians)
    return y_values

def test_plot(x_axis, y_axis):
    print("Start plotting")

    plt.figure(figsize=(10, 5))
    plt.scatter(x_axis, y_axis, label='Voltage over Time', color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title('Time vs Voltage')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

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

time_source, vol_source = create_dummy_data("/Users/deny/proty02/assets/csv/sample2/pfugsumber.csv")
time_sensor, vol_sensor = create_dummy_data("/Users/deny/proty02/assets/csv/sample2/pfugrc.csv")
fitered_vol_sensor = filtering_noise(vol_sensor, 0.0048, -0.0045)
# print(fitered_vol_sensor.tolist())

aligned_degree = aligning_degree(vol_source, 3.5)
new_y = create_dummy_y(aligned_degree, 0.01)

# test_plot(time_array, new_y)
# test_plot(time_sensor, vol_sensor)
# test_plot(aligned_degree, vol_sensor)

test_multi_plot(
    (aligned_degree, new_y, 'source', 'blue'),
    # (aligned_degree, vol_sensor, 'sensor', 'red'),
    (aligned_degree, fitered_vol_sensor, 'sensor', 'red'),
)