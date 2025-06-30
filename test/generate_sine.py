import numpy as np
import matplotlib.pyplot as plt

degrees = np.linspace(0, 360, 360, endpoint=False)
sine_wave = np.sin(np.radians(degrees))

# Plot
plt.plot(degrees, sine_wave)
plt.title("One Full Cycle of Sine Wave")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()