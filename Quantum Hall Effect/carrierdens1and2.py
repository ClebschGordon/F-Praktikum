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
Magnetic= data[:,1]*9/10
time = data[:,0]

#print(np.shape(HallVoltage))
half = int(np.shape(HallVoltage)[0])/2
#print(half) #4898, 4620, 4618, 4560

hallres= HallVoltage[:5000]/Current[:5000]*5000
longres= LongVoltage[:5000]/Current[:5000]*200*10**(-6)/(1.2*10**(-3))*5000    

#plt.plot(time[:], longres[:])
plt.plot(Magnetic[:5000], longres[:5000])
plt.plot(Magnetic[:5000], hallres[:5000])
plt.show()




# Linear method 
def linear_fit_func(m,x,b):
    return m*x+b

params, covariance = curve_fit(linear_fit_func, Magnetic[145:489], hallres[145:489])
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

B=2/(1/Magnetic[1752]+1/Magnetic[2895])
print(carrierden2(2, B))
Btest=Magnetic[int((2895-1752)/2+1752)]
print(carrierden2(2, Btest))


