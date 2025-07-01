import numpy as np

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

def create_dummy_y(aligned_degrees, amplitude):
    radians = np.deg2rad(aligned_degrees)
    y_values = amplitude * np.sin(radians)
    return y_values

def get_max_charge():
    print("something")

def compile_resScope(process, dict_data, max_noise, min_noise):
    results = {}
    for i in range(1, 5):
        if process == "bgn":
            results[f"ch{i}"] = {}
            results[f"ch{i}"]["max"] = float(dict_data[f"ch{i}"].max())
            results[f"ch{i}"]["min"] = float(dict_data[f"ch{i}"].min())
        elif process == "cal":
            results[f"ch{i}"] = float(filter_noise(dict_data[f"ch{i}"], max_noise, min_noise).max())
        elif process == "aqc":
            results[f"ch{i}"] = {}
            




    print(results)
    return results