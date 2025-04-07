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
FieldVoltageup = data[:halfIdx,1]-0.09
FieldVoltagedown = data[halfIdx:,1]+0.09
HallVoltage = data[:,2]*RCurrent
Current = data[:,3]
LongVoltage = data[:,4]*RCurrent*W/L

plt.plot(0.9*FieldVoltageup[:],HallVoltage[:halfIdx]/Current[:halfIdx],label='up')
plt.plot(0.9*FieldVoltagedown[:],HallVoltage[halfIdx:]/Current[halfIdx:])
plt.plot(0.9*FieldVoltageup[:],LongVoltage[:halfIdx]/Current[:halfIdx])
plt.plot(0.9*FieldVoltagedown[:],LongVoltage[halfIdx:]/Current[halfIdx:])
plt.legend()


with open("Data_Nick_Salah/4.dat", "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

halfIdx = int(len(data[:,1])/2)
FieldVoltageup = data[:halfIdx,1]-0.09
FieldVoltagedown = data[halfIdx:,1]+0.09
HallVoltage = data[:,3]*RCurrent
Current = data[:,2]
LongVoltage = data[:,4]*RCurrent*W/L

plt.plot(0.9*FieldVoltageup[:],HallVoltage[:halfIdx]/Current[:halfIdx],label='up')
plt.plot(0.9*FieldVoltagedown[:],HallVoltage[halfIdx:]/Current[halfIdx:])
plt.plot(0.9*FieldVoltageup[:],LongVoltage[:halfIdx]/Current[:halfIdx])
plt.plot(0.9*FieldVoltagedown[:],LongVoltage[halfIdx:]/Current[halfIdx:])
plt.legend()

plt.show()

value2=25812.80745/25395.582
print(25812.80745/25960.382)
print(value2)

array = np.array([25389.21,
25433.232,
25449.544,
25398.762,
25287.358,
25398.531,
25425.456,
25409.288,
25503.775,
25630.971])
array2 = np.array([
25389.212,
25433.232,
25449.544 ,
25398.762 ,
25287.358 ])
print(array*value2)
print(array2*value2)