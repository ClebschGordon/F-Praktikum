import matplotlib.pyplot as plt
import numpy as np
import io
from scipy.optimize import curve_fit

# 67 , 60 , 64 , 50

file_path = "Data_Nick_Salah/0.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)


HallVoltage = data[:,2]
LongVoltage = data[:,4]
Current = data[:,3]
Magnetic= data[:,1]*9/10
time = data[:,0]

hallres= HallVoltage[:]/Current[:]*5000
longres= LongVoltage[:]/Current[:]*200*10**(-6)/(1.2*10**(-3))*5000   

#conductivity
conduct = 1/longres[50]
print(conduct)

file_path = "dataeval.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=1)

method1 = data[:,1]
method2 = data[:,2]
method3 = data[:,3]
cond = data[:,4]
Rh = data[:,5]

#Hall Resistance
e = 1.602e-19  # Elementarladung
Hallresist = 1/(e*method1*10**(15))

print(Hallresist)

#mu

mu=cond[:]*Rh[:]
print(mu)
