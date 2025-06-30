import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# path = "/Users/deny/proty02/assets/csv/sample.csv"
# path = "/Users/deny/proty02/assets/csv/sample1/pfutsumber.csv"
path = "/Users/deny/proty02/assets/csv/sample2/pfugsumber.csv"

df = pd.read_csv(path, header=None, usecols=[3, 4], names=['Time', 'Vol'])
df = df.dropna()
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
df['Vol'] = pd.to_numeric(df['Vol'], errors='coerce')
df = df.dropna()
# print(df)

time_array = df['Time'].to_numpy()
vol_array = df['Vol'].to_numpy()

print("Time:", time_array)
print("Vol:", vol_array)

"""
plt.figure(figsize=(10, 5))
plt.scatter(time_array, vol_array, label='Voltage over Time', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Time vs Voltage')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
"""

num_rows = 87500
num_waves = 3.5
rows_per_cycle = num_rows / num_waves
degrees_per_row = 360 / rows_per_cycle

index_max = np.argmax(vol_array[:int(rows_per_cycle)])

# def compute_aligned_degrees(index):
#     relative_index = index - index_max  # shift so max_index becomes 0
#     degree = 90 + (relative_index * degrees_per_row)  # align to 90°
#     return degree % 360

# df['aligned_degree'] = df.index.to_series().apply(compute_aligned_degrees)

# amplitude = 50
# df['new_y'] = amplitude * np.sin(np.radians(df['aligned_degree']))


indices = np.arange(num_rows)
relative_indices = indices - index_max
aligned_degrees = (90 + relative_indices * degrees_per_row) % 360

radians = np.deg2rad(aligned_degrees)
y_values = 100 * np.sin(radians)

# print(aligned_degrees)

plt.figure(figsize=(10, 5))
# plt.scatter(df['Time'], df['Vol'], label='Voltage over Time', color='blue')
# plt.scatter(df['Time'], df['new_y'], label='Voltage over Time', color='blue')
plt.scatter(time_array, y_values, label='Voltage over Time', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Time vs Voltage')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# print(df)