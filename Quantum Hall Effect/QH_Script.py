import matplotlib.pyplot as plt
import numpy as np
import io

file_path = "Data_Nick_Salah/6.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15,skip_footer=131)
# The last 130ish datapoints are skipped because we cannot convertet them into temperatures using the ITS-90

HallVoltage = data[:,3]
LongVoltage = data[:,4]
Current = data[:,2]
print(np.shape(HallVoltage))
half = int(np.shape(HallVoltage)[0])/2
print(half)


plt.plot(HallVoltage[:]/Current[:])
plt.plot(LongVoltage[:]/Current[:])
plt.plot(HallVoltage[::-1]/Current[::-1])
plt.show()