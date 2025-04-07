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

file_path = f"Data_Nick_Salah/4.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data2 = np.genfromtxt(io.StringIO(processed_text), skip_header=15)
# The last 130ish datapoints are skipped because we cannot convertet them into temperatures using the ITS-90
RCurrent = 4.982e3
W = 200e-6
L = 1.2e-3
HallVoltage = data[:,2]
LongVoltage = data[:,4]
Current = data[:,3]
FieldStrength = data[:,1]
Time = data[:,0]
HallVoltage2 = data2[:,3]
Current2 = data2[:,2]
print(np.shape(HallVoltage))
half = int(np.shape(HallVoltage)[0])/2
print(np.round(half))
halfIdx = int(np.round(half))

def DeterminePlateauValue(idx1,idx2):
    sum=0
    for i,e in enumerate(HallVoltage[idx1:idx2]):
        sum += e*RCurrent/Current[idx1+i]
        print("Test")
        print(e)
        print(Current[idx1+i])
    return(sum/(idx2-idx1))

one = 3538
two = 4447
idx = 1
if False:
    print(str(DeterminePlateauValue(one,two))+'+-'+str(DeterminePlateauValue(one,two)*0.02)+'|'+str(idx*DeterminePlateauValue(one,two))+'+-'+str(idx*DeterminePlateauValue(one,two)*0.02))
    ResistanceVal = DeterminePlateauValue(one,two)
    ResistanceErr = DeterminePlateauValue(one,two)*0.02
    VonKlitzingVal =idx*ResistanceVal
    VonKlitzingErr = idx*ResistanceErr
    with open("out/VonKlitzingData.dat", "a") as file:
        file.write(f"({ResistanceVal:.3f}+-{ResistanceErr:.3f})  ({VonKlitzingVal:.3f} {VonKlitzingErr:.3f})\n")
#plt.plot(HallVoltage[:halfIdx]/Current[:halfIdx],label='up')
#plt.plot(HallVoltage2[130:halfIdx]/Current2[130:halfIdx])
#value1 = HallVoltage[4051]/Current[4051]
#value2 = HallVoltage2[4051]/Current[4051+130]

#plt.plot(LongVoltage[:halfIdx]/Current[:halfIdx])
#plt.plot(HallVoltage[::-1]/Current[::-1],label='down')
#plt.scatter(Time[one:two],HallVoltage[one:two]/Current[one:two],s=1,color='black')
plt.legend()
plt.show()
# Example data
x = FieldStrength[:halfIdx]
y1 = HallVoltage[:halfIdx]*RCurrent/Current[:halfIdx] * math.pow(10,-3)
y2 = LongVoltage[:halfIdx]*RCurrent*W/(Current[:halfIdx]*L) * math.pow(10,-3)
# Create base figure and axis
fig, ax1 = plt.subplots()

# Plot first dataset
ax1.plot(x, y1, 'b-', label='R$_{xx}$', linewidth=2)
ax1.set_xlabel('B[T]')
ax1.set_ylabel('R$_{xx}$', color='b')
ax1.tick_params(axis='y', labelcolor='b',direction='in')
ax1.set_ylim(0,27)
ax1.set_xlim(0,9)
ax1.tick_params(axis='both', direction='in', top=True, right=True, which='both', labelcolor='black')

# Create second y-axis sharing the same x-axis
ax2 = ax1.twinx()
ax2.plot(x, y2, 'r-', label='R$_{xy}$', linewidth=2)
ax2.set_ylabel('R$_{xy}$', color='r')
ax2.tick_params(axis='y', labelcolor='r',direction='in')
ax2.set_ylim(0,y2.max()+y2.max()*0.01)
ax2.set_xlim(0,9)

# Optional: add title or legend

# Show the plot

plt.savefig(f"out/InitialMeasurement_Data{DataSet}.png",dpi=300, bbox_inches='tight', pad_inches=0.01)