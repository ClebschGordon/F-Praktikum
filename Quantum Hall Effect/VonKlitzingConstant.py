import math
from uncertainties import ufloat
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import io

DataSet = 4
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
RCurrent = 5.0e3
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
        sum += e/Current[idx1+i]
        #print("Test")
        #print(e)
        #print(Current[idx1+i])
    return(sum/(idx2-idx1))

one = 960
two = 987
idx = 5
if False:
    print(str(DeterminePlateauValue(one,two))+'+-'+str(DeterminePlateauValue(one,two)*0.02)+'|'+str(idx*DeterminePlateauValue(one,two))+'+-'+str(idx*DeterminePlateauValue(one,two)*0.02))
    ResistanceVal = DeterminePlateauValue(one,two)*RCurrent
    ResistanceErr = ResistanceVal*np.sqrt(0.01**2+0.01**2)#The addition of the squares of the relative errors of the R_I
    VonKlitzingVal =idx*ResistanceVal
    VonKlitzingErr = idx*ResistanceErr
    print(VonKlitzingVal,VonKlitzingErr)
    with open("out/VonKlitzingData.dat", "a") as file:
        file.write(f"({ResistanceVal:.3f}+-{ResistanceErr:.3f})  ({VonKlitzingVal:.3f} {VonKlitzingErr:.3f})\n")
#plt.plot(HallVoltage[:halfIdx]/Current[:halfIdx],label='up')
#plt.plot(HallVoltage2[130:halfIdx]/Current2[130:halfIdx])
#value1 = HallVoltage[4051]/Current[4051]
#value2 = HallVoltage2[4051]/Current[4051+130]
plt.show()
#plt.plot(LongVoltage[:halfIdx]/Current[:halfIdx])
#plt.plot(HallVoltage[::-1]/Current[::-1],label='down')
#plt.scatter(Time[one:two],HallVoltage[one:two]/Current[one:two],s=1,color='black')
#plt.legend()
#plt.show()
# Example data
x = FieldStrength[:halfIdx]
y1 = HallVoltage[:halfIdx]*RCurrent/Current[:halfIdx] * math.pow(10,-3)
y2 = LongVoltage[:halfIdx]*RCurrent*W/(Current[:halfIdx]*L) * math.pow(10,-3)
# Create base figure and axis
fig, ax1 = plt.subplots()

# Plot first dataset
line1, = ax1.plot(x, y1, 'b-', label=r'Hall resistivity $\rho_{xy}$', linewidth=2)
ax1.set_xlabel('B[T]')
ax1.set_ylabel(r'$\rho_{xy}[k\Omega]$', color='b')
ax1.tick_params(axis='y', colors='b',direction='in')
ax1.set_ylim(0,27)
ax1.set_xlim(0,9)
ax1.tick_params(axis='both', direction='in', top=True, right=True, which='both', labelcolor='black')

# Create second y-axis sharing the same x-axis
ax2 = ax1.twinx()
line2, = ax2.plot(x, y2, 'r-', label=r'Longitudinal resistivity $\rho_{xx}$', linewidth=2)
ax2.set_ylabel(r'$\rho_{xx}[k\Omega]$', color='r')
ax2.tick_params(axis='y', labelcolor='r',direction='in')
ax2.set_ylim(0,y2.max()+y2.max()*0.01)
ax2.set_xlim(0,9)

# Optional: add title or legend
custom_text = Line2D([0], [0], color='none', label=r'T = $1.515\,K\,\,U_G = -0.25\,$V')
#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6), constrained_layout=True
fig.legend(handles=[custom_text,line1,line2],loc='lower left',bbox_to_anchor=(0.12,0.68))
plt.show()
# Show the plot
#plt.savefig(f"out/InitialMeasurement_Data{DataSet}.png",dpi=300, bbox_inches='tight', pad_inches=0.01)
