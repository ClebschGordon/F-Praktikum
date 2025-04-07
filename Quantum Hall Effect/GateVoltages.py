import math

from matplotlib.lines import Line2D
from uncertainties import ufloat
import matplotlib.pyplot as plt
import numpy as np
import io

DataSet = 6
file_path = f"Data_Nick_Salah/{DataSet}.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

RCurrent = 4.982e3
W = 200e-6
L = 1.2e-3


Field = data[:,1]
Current = data[:,2]
HallVoltage = data[:,3]
LongVoltage = data[:,4]

half = int(np.shape(HallVoltage)[0])/2
print(np.round(half))
halfIdx = int(np.round(half))


x = 0.9*Field[:halfIdx]
y1 = HallVoltage[:halfIdx]*RCurrent/Current[:halfIdx] * math.pow(10,-3)
y2 = LongVoltage[:halfIdx]*RCurrent*W/(Current[:halfIdx]*L) * math.pow(10,-3)
# Create base figure and axis
fig, ax1 = plt.subplots()

# Plot first dataset
line1, = ax1.plot(x, y1, 'b-', label=r'Hall resitivity $\rho_{xy}$', linewidth=2)
ax1.set_xlabel('B[T]')
ax1.set_ylabel(r'$\rho_{xy}[k\Omega]$')
ax1.tick_params(axis='y', colors='blue',direction='in',labelcolor='blue')
ax1.spines['left'].set_color('blue')
ax1.set_ylim(0,12)
ax1.set_xlim(0,9)
ax1.tick_params(axis='both', direction='in', top=True, which='both', labelcolor='black')

# Create second y-axis sharing the same x-axis
ax2 = ax1.twinx()
line2, = ax2.plot(x, y2, 'r-', label=r'Longitudinal resistivity $\rho_{xx}$', linewidth=2)
ax2.set_ylabel(r'$\rho_{xx}[k\Omega]$')
ax2.spines['right'].set_color('red')
ax2.tick_params(axis='y',labelcolor='r',direction='in')
ax2.set_ylim(0,y2.max()+y2.max()*0.05)
ax2.set_xlim(0,9)

# Optional: add title or legend

# Show the plot
custom_text = Line2D([0], [0], color='none', label=r'T = $1.515\,K\,\,U_G = 1.00\,$V')
#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6), constrained_layout=True
fig.legend(handles=[custom_text,line1,line2],loc='lower left',bbox_to_anchor=(0.12,0.68))
plt.show()
#plt.savefig(f"out/GateVoltage_Data{-2}V.png",dpi=300, bbox_inches='tight', pad_inches=0.01)