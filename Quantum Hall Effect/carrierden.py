import matplotlib.pyplot as plt
import numpy as np
import io
from scipy.optimize import curve_fit

file_path = "Data_Nick_Salah/1.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)
# The last 130ish datapoints are skipped because we cannot convertet them into temperatures using the ITS-90

HallVoltage = data[:,2]
LongVoltage = data[:,4]
Current = data[:,3]
Magnetic= data[:,1]
time = data[:,0]

hallres= HallVoltage[:]/Current[:]*1000
longres= LongVoltage[:]/Current[:]*200*10**(-6)/(1.2*10**(-3))*1000    

#plt.plot(time[:], longres[:])
plt.plot(time[:], hallres[:])
#plt.plot(Magnetic[68:493], LongVoltage[68:493]/Current[68:493])
plt.show()




# Linear method 
def linear_fit_func(m,x,b):
    return m*x+b

params, covariance = curve_fit(linear_fit_func, Magnetic[149:493], hallres[149:493])
m1, b1 = params

x_fit_mfield = np.linspace(0, 9, 100)
y_fit_res = linear_fit_func(x_fit_mfield,m1,b1)

def carrierden1(slope):
    return 1/(slope*1.602*10**(-19))

print(carrierden1(m1))

plt.plot(x_fit_mfield, y_fit_res, color = 'black', label='Quadratischer Fit')
plt.show()
m=0
# Filling Factor method
for i in longres:
        m +=1
        if max(longres)==i:
            print(i,time[m])

def carrierden2(filling, B):
     return filling/(6.626*10**(-34))*1.602*10**(-19)*B

77+216
190,6+4350
B=2/(1/Magnetic[770+2160]+1/Magnetic[1906+4350])
print(carrierden2(1, B))
Btest=Magnetic[int((1906+4350-770+2160)/2+770+2160)]
print(carrierden2(1, Btest))
