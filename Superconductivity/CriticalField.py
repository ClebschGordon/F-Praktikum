import math

import numpy as np
import io
import matplotlib.pyplot as plt
file_path = "Nick_Salah/Nick_Sala_SC_20.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)
time = data[:,0]
Voltage = data[:,1]
FieldStrength = data[:,4]
AllanBradley = data[:,3]
#plt.plot(time[:],FieldStrength[:])
#plt.show()
plt.plot(time[:],Voltage[:])
plt.axvline(time[50],color='red')
plt.axvline(time[63],color='red')
plt.axvline(time[115],color='red')
print(FieldStrength[12],FieldStrength[63],FieldStrength[115])
plt.show()
plt.plot(time[:],FieldStrength[:])
plt.axhline(FieldStrength[50],color='red')
plt.axhline(FieldStrength[63],color='red')
plt.axhline(FieldStrength[115],color='red')
#plt.show()

from Supercond_Script import AllanBradleyToTemp
temp = AllanBradleyToTemp(AllanBradley[50],True)
print("halla")
print(temp[0],52.9*FieldStrength[50]/(384.5*math.pow(10,-6)))

# Data seems to be fitting, but now we first need to average over all the peaks in order to get the real result
