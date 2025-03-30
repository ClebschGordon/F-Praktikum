import numpy as np
import io
import matplotlib.pyplot as plt
file_path = "Nick_Salah/Nick_Sala_SC_5.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)
time = data[:,0]
Voltage = data[:,1]
plt.plot(time[:],Voltage[:])
plt.show()
