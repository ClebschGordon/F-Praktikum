import math
import numpy as np
import io
import matplotlib.pyplot as plt
file_path = "Nick_Salah/Nick_Sala_SC_24.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

from Supercond_Script import AllanBradleyToTemp
AllanBradley = data[:,3]
voltage = data[:,1]
print(AllanBradleyToTemp(0.0112,True))
plt.plot(AllanBradleyToTemp(AllanBradley[:],True),voltage[:])
plt.show()

