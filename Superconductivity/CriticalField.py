import math

import numpy as np
import io
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


file_path = "Nick_Salah/Nick_Sala_SC_14.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)
time = data[:,0]
Voltage = data[:,1]
FieldStrength = data[:,4]
AllanBradley = data[:,3]
#plt.plot(time[:],Voltage[:])
#plt.show()

#Import for manual analysis
from Supercond_Script import AllanBradleyToTemp

def errorfieldhigh(fstrength):
    errfield = 54.1*fstrength/(384.5*math.pow(10,-6))
    return errfield

def errorfieldlow(fstrength):
    errfield = 51.7*fstrength/(384.5*math.pow(10,-6))
    return errfield

def fieldstr(fstre):
    fieldst = 52.9*fstre/(384.5*math.pow(10,-6))
    return fieldst



avgfh= errorfieldhigh(FieldStrength[181])
avgfl= errorfieldlow(FieldStrength[181])
print(avgfl)
print(avgfh)

avgth = AllanBradleyToTemp(AllanBradley[181], True)[1]
avgtl = AllanBradleyToTemp(AllanBradley[181], True)[2]
#print(avgth,avgtl)
#print(AllanBradleyToTemp(AllanBradley[16], True),AllanBradleyToTemp(AllanBradley[16], False))

# Data seems to be fitting, but now we first need to average over all the peaks in order to get the real result



#Import manual gathered data
file_path = "critfield.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=4)

avgtemp = data[:,1]
avgfield = data[:,2]
ErrorTemphigh = data[:,3]

#Import manual gathered data
file_path = "errod.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=4)

ErrorTemplow = data[:,0]
ErrorFieldhigh = data[:,1]
ErrorFieldlow = data[:,2]

# Define a quadratic func (y = Hc(1-(T/Tc)**2))
def quadratic_func(T, Hc, Tc):
    return  Hc*(1-(T/Tc)**2)

# Fit the data to the linear function
params, covariance = curve_fit(quadratic_func, avgtemp, avgfield)
Hc, Tc = params

params, covariance = curve_fit(quadratic_func, avgtemp, ErrorFieldhigh)
Hch, Tch = params

params, covariance = curve_fit(quadratic_func, avgtemp, ErrorFieldlow)
Hcl, Tcl = params

print(Hc,Tc,Hch -Hc ,Tc - Tch ,Hcl - Hc,Tcl - Tc)
# Errors for temp and field

YErrorhigh= ErrorFieldhigh - avgfield
YErrorlow= avgfield - ErrorFieldlow

plt.errorbar(avgtemp,avgfield,yerr=YErrorhigh,xerr=ErrorTemphigh, ecolor='green', fmt='NONE', label = 'Fehler der Messdaten')
plt.errorbar(avgtemp,avgfield,yerr=YErrorlow,xerr=ErrorTemplow, ecolor='green', fmt='NONE')


# Generate fitted values
x_fit_temp = np.linspace(0, 3.74, 100)
y_fit_field = quadratic_func(x_fit_temp,Hc, Tc)

y_fit_highfield = quadratic_func(x_fit_temp,Hch, Tch)

y_fit_lowfield = quadratic_func(x_fit_temp,Hcl, Tcl)

#Plot data and fitted line
plt.xlim(0,4)
plt.ylim(0,30)

plt.scatter(avgtemp, avgfield, label='Messdaten', color='black', s= 1)
plt.plot(x_fit_temp, y_fit_field, color = 'black', label='Quadratischer Fit')

#plt.scatter(avgtemp, ErrorFieldhigh, label='Data', color='blue')
plt.plot(x_fit_temp, y_fit_highfield, color = 'red', ls= '--', lw=1 , label = "Quadratischer Fit für obere Fehlergrenze")

#plt.scatter(avgtemp, ErrorFieldlow, label='Data', color='green')
plt.plot(x_fit_temp, y_fit_lowfield, color = 'blue', ls= '--', lw=1, label = "Quadratischer Fit für untere Fehlergrenze")
plt.tick_params(axis='both', which='both', direction='in', length=4, width=2,
               top=True, bottom=True, left=True, right=True)
plt.xlabel('Temperatur (K)')
plt.ylabel('Magnetisches Feld (kA/m)')
plt.legend()
plt.grid()
plt.show()