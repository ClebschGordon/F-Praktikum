import math
from uncertainties import ufloat
import matplotlib.pyplot as plt
import numpy as np
import io

DataSet = 3
file_path = f"Data_Nick_Salah/{DataSet}.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

RCurrent = 4.982e3
W = 200e-6
L = 1.2e-3

halfIdx = int(len(data[:,1])/2)
FieldVoltage = data[:,1]
HallVoltage = data[:,2]*RCurrent
Current = data[:,3]
LongVoltage = data[:,4]*RCurrent*W/L


with open("Data_Nick_Salah/4.dat", "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data2 = np.genfromtxt(io.StringIO(processed_text), skip_header=15)


FieldVoltage2 = data2[:,1]
HallVoltage2 = data2[:,3]*RCurrent
Current2 = data2[:,2]
LongVoltage2 = data2[:,4]*RCurrent*W/L

plt.plot(FieldVoltage,HallVoltage/Current)
plt.plot(FieldVoltage2,HallVoltage2/Current2)
plt.show()

value2 = 25.964e3
value1 = 25.524e3

print(np.sqrt(value2/value1))
factor = np.sqrt(value2/value1)
relError = 0.015/4.982
print(relError*100)
print(25.520*factor,25.520*factor*relError)
print(1-factor)

