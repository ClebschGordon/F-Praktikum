import math

from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
from uncertainties import ufloat
import matplotlib.pyplot as plt
import numpy as np
import io

DataSet = 1
file_path = f"Data_Nick_Salah/{DataSet}.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

RCurrent = 5.0e3
W = 200e-6
L = 1.2e-3


Field = data[:,1]#*0.9
Current = data[:,3]
HallVoltage = data[:,2]
LongVoltage = data[:,4]


half = int(np.shape(HallVoltage)[0])/2
print(np.round(half))
halfIdx = int(np.round(half))


x = Field[:halfIdx]#*0.9
y1 = HallVoltage[:halfIdx]*RCurrent/Current[:halfIdx] * math.pow(10,-3)
y2 = LongVoltage[:halfIdx]*RCurrent*W/(Current[:halfIdx]*L) * math.pow(10,-3)
#plt.scatter(x,y1,s=1)
#plt.scatter(x,y2,s=1)
#plt.show()
# Create base figure and axis
fig, ax1 = plt.subplots()

# Plot first dataset
line1, = ax1.plot(x, y1, 'b-', label=r'Hall resitivity $\rho_{xy}$', linewidth=2)
ax1.set_xlabel('B[T]')
ax1.set_ylabel(r'$\rho_{xy}[k\Omega]$',color='b')
ax1.tick_params(axis='y', colors='blue',direction='in',labelcolor='blue')
ax1.spines['left'].set_color('blue')
#ax1.set_ylim(-30,5)
ax1.set_xlim(0,9)
ax1.tick_params(axis='both', direction='in', top=True, which='both', labelcolor='black')

# Create second y-axis sharing the same x-axis
ax2 = ax1.twinx()
line2, = ax2.plot(x, y2, 'r-', label=r'Longitudinal resistivity $\rho_{xx}$', linewidth=2)
ax2.set_ylabel(r'$\rho_{xx}[k\Omega]$',color='red')
ax2.spines['right'].set_color('red')
ax2.tick_params(axis='y',labelcolor='r',direction='in')
ax2.set_ylim(-0.5,y2.max()+y2.max()*0.05)
ax2.set_xlim(0,9)



# Show the plot
custom_text = Line2D([0], [0], color='none', label=r'T = $1.515\,K\,\,U_G = -1.00\,$V')
#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6), constrained_layout=True
fig.legend(handles=[custom_text,line1,line2],loc='lower left',bbox_to_anchor=(0.12,0.4))
plt.show()
#plt.savefig(f"out/GateVoltage_Data{-1}V.png",dpi=300, bbox_inches='tight', pad_inches=0.01)


def linearFit(B,a,m):
    return a*B+m

params, covariance = curve_fit(linearFit,Field[10:500],HallVoltage[10:500]*RCurrent/(Current[10:500]))
grad,m = params
print(params)
print(format(1/(grad * 1.60217e-19), ".5e"))
plt.plot(Field[:halfIdx],HallVoltage[:halfIdx]*RCurrent/(Current[:halfIdx]))
x = np.linspace(0,1,100)
y = linearFit(x,grad,m)
plt.plot(x,y)
plt.show()