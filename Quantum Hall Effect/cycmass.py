import matplotlib.pyplot as plt
import numpy as np
import io
from scipy.optimize import curve_fit

file_path = "Data_Nick_Salah/3.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

half = int(len(data[:,1])/2)
HallVoltage = data[:,2]
LongVoltage = data[:,4]
Current = data[:,3]
Magneticup= data[:half,1]*9/10-0.08
Magneticdown= data[half:,1]*9/10+0.08
time = data[:,0]

Magnetic = data[:,1]

#defining Hallresistivity and longitudinal resistivity
hallres= HallVoltage[:]/Current[:]*5000
longres= LongVoltage[:]/Current[:]*200*10**(-6)/(1.2*10**(-3))*5000   

#PLotting longitudinal resistivity for up and down sweep
plt.plot(Magnetic[:],longres[:])
plt.plot(Magneticup[:],longres[:half])
plt.show()

#konstants
hbar = 1.055*10**(-34)
e = 1.602*10**(-19)
me = 9.113*10**(-31)
pi = 3.142
kb = 1.381*10**(-23)

#defining function for the ratio between cyclotronmass and electron mass
def mctomeratio(Magneticfield, Temperaturehigh, Amplitudehigh, Amplitudesmall):
     return hbar*e*Magneticfield/(me*pi**2*kb*Temperaturehigh)*np.arccosh(Amplitudesmall/Amplitudehigh)

#defining fit curve for the prefactor
def lorentz_curve(B , a , b):
     return a/(1+(B*b)**2)

#defining longitudinal conductivity
longcon = longres/(longres**2+hallres**2)

ind_start = np.argmax(Magneticup>0.6)
ind_end = np.argmax(Magneticup>1.2)

#fitting to conductivity for up sweep
params, covariance = curve_fit(lorentz_curve, Magneticup[ind_start:ind_end], longcon[ind_start:ind_end]) # use 4898 for 4.06K
m1, b1 = params

x_fit_sfield = np.linspace(0, 9, 100)
y_fit_res = lorentz_curve(Magnetic[:],m1,b1)

print(m1, b1)

#deviding conductivity with lorentzfunction to get only the oscillatin part
longconlor= longcon[:]/(m1/(1+(b1*Magnetic[:])**2)) # use 4898 for 4.06K

#plottin the oscillating part
plt.plot(Magneticup[ind_start:ind_end], longconlor[ind_start:ind_end])
plt.show()

#searching for max/min in a given B-field range
#2-2.5T

print(max(longconlor[ind_start:ind_end]),min(longconlor[ind_start:ind_end])) # use 841 and 1232 for 4.06K
#for 4.06K 0.8482260193219099 0.2210450080120738 -> Amp : 0.3135 0.121

#for 2.1K 0.6577411469835687 0.13519901241072224 -> Amp : 0.2615 0.151

print(mctomeratio(1.13,3.1, 0.121, 0.151))
