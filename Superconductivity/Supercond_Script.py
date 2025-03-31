import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import io

# File path
file_path = "Nick_Salah/Nick_Sala_SC_0.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15,skip_footer=131)
# The last 130ish datapoints are skipped because we cannot convertet them into temperatures using the ITS-90

# Extract columns
col1 = data[:, 0]
col2 = data[:, 1]
col3 = data[:, 2]
col4 = data[:, 3]
col5 = data[:, 4]

plt.plot(data[:,2],data[:,3])
#plt.show()

# File path
file_path = "Nick_Salah/Calibration.dat"  # Update with actual file path

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=3)

# Extract columns (X in Volts, Y in mBar)
x_data_volts = data[:, 1]  # X values in Volts
y_data_mbar = data[:, 0]   # Y values in mBar

# Define a linear function (y = mx + b)
def linear_func(x, m, b):
    return m * x + b

# Fit the data to the linear function
params, covariance = curve_fit(linear_func, x_data_volts, y_data_mbar)
m, b = params  # Extract slope (mBar/V) and intercept (mBar)

# Calculate the errors (standard deviations) of the parameters
errors = np.sqrt(np.diag(covariance))
m_error, b_error = errors  # Error in slope and intercept

# Generate fitted values
x_fit_volts = np.linspace(min(x_data_volts), max(x_data_volts), 100)
y_fit_mbar = linear_func(x_fit_volts, m, b)

# Plot data and fitted line
#plt.scatter(x_data_volts, y_data_mbar, label='Data', color='red')
#plt.plot(x_fit_volts, y_fit_mbar, label=f'Fit: P = {m:.2e} * V + {b:.2e}', color='blue')
#plt.xlabel('Voltage (V)')
#plt.ylabel('Pressure (mBar)')
#plt.legend()
#plt.title('Linear Fit: Voltage vs. Pressure')
#plt.show()

# Print fitted parameters and their errors
print(f"Fitted parameters and errors:")
print(f"Slope (mBar/V) = {m:.4e} ± {m_error:.4e}")
print(f"Intercept (mBar) = {b:.4e} ± {b_error:.4e}")

# These fit parameters will now be used to calculate the pressure from the recorded Voltages (column: U_Manometer).
def linearDependence(Voltage):
    return m*Voltage + b
#
from TemperatureCalibration import pressure_to_temperature
LambdaPointidx = 2235
cutoffPoint = 2460
temp_above = pressure_to_temperature(linearDependence(col3[:LambdaPointidx]),True)
temp_below = pressure_to_temperature(linearDependence(col3[LambdaPointidx:cutoffPoint]),False)
temp_belowForPlot = pressure_to_temperature(linearDependence(col3[LambdaPointidx:]),False)
temp = np.append(temp_above,temp_below)
tempForPlot = np.append(temp_above,temp_belowForPlot)

plt.scatter(tempForPlot[:],col4[:],s=5)

def expoFit(x,U0,C,d):
    return U0*np.exp(C/x) + d

expoParamsAbove, Expocovariance = curve_fit(expoFit, temp_above, col4[:LambdaPointidx],p0=[4,10,-4],maxfev=5000)
print(expoParamsAbove)
U0,C,d = expoParamsAbove
expoParamsBelow, ExpocovarianceBelow = curve_fit(expoFit,temp_below,col4[LambdaPointidx:cutoffPoint],p0=[9,4,-17],maxfev=5000)
print(expoParamsBelow)
U0Bel,CBel,dBel = expoParamsBelow

x = np.linspace(temp_above[0],temp_above[LambdaPointidx-1],100)
plt.plot(x,expoFit(x,U0,C,d),color='red')

xb = np.linspace(temp[LambdaPointidx],temp[cutoffPoint-1],100)
plt.plot(xb,expoFit(xb,U0Bel,CBel,dBel),color='red')
plt.show()


def AllanBradleyToTemp(U,isAboveLambda):
    if isAboveLambda:
        return C/np.log((U-d)/U0)
    else:
        return CBel/np.log((U-dBel)/U0Bel)



AllanBradleyAbove = AllanBradleyToTemp(col4[:LambdaPointidx],True)
AllanBradleyBelow = AllanBradleyToTemp(col4[LambdaPointidx:cutoffPoint],False)
#print(AllanBradleyBelow)
#print(AllanBradleyAbove)






