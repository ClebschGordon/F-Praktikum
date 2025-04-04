import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

#plt.plot(data[:,2],data[:,3])
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
#print(f"Fitted parameters and errors:")
#print(f"Slope (mBar/V) = {m:.4e} ± {m_error:.4e}")
#print(f"Intercept (mBar) = {b:.4e} ± {b_error:.4e}")


# These fit parameters will now be used to calculate the pressure from the recorded Voltages (column: U_Manometer).
def linearDependence(Voltage):
    return m*Voltage + b
#
from TemperatureCalibration import pressure_to_temperature
LambdaPointidx = 2230
cutoffPoint = 2400
temp_above = pressure_to_temperature(linearDependence(col3[:LambdaPointidx]),True)
temp_below = pressure_to_temperature(linearDependence(col3[LambdaPointidx:cutoffPoint]),False)
temp_belowForPlot = pressure_to_temperature(linearDependence(col3[LambdaPointidx:]),False)
temp = np.append(temp_above,temp_below)
tempForPlot = np.append(temp_above,temp_belowForPlot)

# Now we also need to fit the error bars of the data in order to calculate the errors of the fit parameters
pressureErrors_above = linearDependence(col3[:LambdaPointidx]) + linearDependence(col3[:LambdaPointidx])*0.03 + 1
temperatureErrors_above = pressure_to_temperature(pressureErrors_above,True)

pressureErrors_above_below = linearDependence(col3[:LambdaPointidx]) - linearDependence(col3[:LambdaPointidx])*0.03 - 1
temperatureError_above_below = pressure_to_temperature(pressureErrors_above_below,True)

pressureErrors_below = linearDependence(col3[LambdaPointidx:]) + linearDependence(col3[LambdaPointidx:])*0.03 + 1
temperatureErrors_below = pressure_to_temperature(pressureErrors_below,False)

pressureErrors_below_below = linearDependence(col3[LambdaPointidx:]) - linearDependence(col3[LambdaPointidx:])*0.03 - 1
temperatureErrors_below_below = pressure_to_temperature(pressureErrors_below_below,False)

def expoFit(x,U0,C,d):
    return U0*np.exp(C/x) + d


expoParamsAbove, Expocovariance = curve_fit(expoFit, temp_above, col4[:LambdaPointidx],p0=[0.00432,4.84,-0.00434],maxfev=5000)
print(expoParamsAbove)
U0,C,d = expoParamsAbove

errorAboveParams, covariance = curve_fit(expoFit,temperatureErrors_above,col4[:LambdaPointidx],p0=[0.00432,4.84,-0.00434],maxfev=5000)
U0ErrAbove,CErrAbove,dErrAbove = errorAboveParams
print("error" + str(errorAboveParams))
errorAboveParamsBelow, covariance = curve_fit(expoFit,temperatureError_above_below,col4[:LambdaPointidx],p0=[0.00432,4.84,-0.00434],maxfev=5000)
U0ErrAboveBelow,CErrAboveBelow,dErrAboveBelow = errorAboveParamsBelow
print("errorBelow"+str(errorAboveParamsBelow))

########################### Below the Lambda Point ####################################

expoParamsBelow, ExpocovarianceBelow = curve_fit(expoFit,temp_below,col4[LambdaPointidx:cutoffPoint],p0=[9,4,-17],maxfev=5000)
print(expoParamsBelow)
U0Bel,CBel,dBel = expoParamsBelow

errorBelowParams, covariance = curve_fit(expoFit,temperatureErrors_below[:(cutoffPoint-LambdaPointidx)],col4[LambdaPointidx:cutoffPoint],p0=[9,4,-17],maxfev=5000)
print("error"+str(errorBelowParams))
U0ErrBelow,CErrBelow,dErrBelow = errorBelowParams
errorBelowParamsBelow, covariance = curve_fit(expoFit,temperatureErrors_below_below[:(cutoffPoint-LambdaPointidx)],col4[LambdaPointidx:cutoffPoint],p0=[9,4,-17],maxfev=5000)
print("errorBelow"+str(errorBelowParamsBelow))
U0ErrBelowBelow,CErrBelowBelow,dErrBelowBelow = errorBelowParamsBelow

print(expoParamsAbove,errorAboveParams-expoParamsAbove,expoParamsAbove-errorAboveParamsBelow)
print(expoParamsBelow,errorBelowParams-expoParamsBelow,expoParamsBelow-errorBelowParamsBelow)
plt.scatter(tempForPlot[:],col4[:],color='lightblue',s=1,label='Messdaten')
plt.plot(temperatureErrors_below_below[:-1],col4[LambdaPointidx:-1],color='grey')
plt.plot(temperatureErrors_below,col4[LambdaPointidx:],color='grey',label='Fehlerbalken')


x = np.linspace(temp_above[0],temp_above[LambdaPointidx-1],100)
plt.plot(x,expoFit(x,U0,C,d),color='red',label='Exp. Fit für T>$T_\lambda$')

xb = np.linspace(temp[LambdaPointidx],temp[cutoffPoint-1],100)
plt.plot(xb,expoFit(xb,U0Bel,CBel,dBel),color='blue',label='Exp. Fit für T<$T_\lambda$')

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x * 1000:.0f}"))
plt.ylabel("Spannung $U_k$ [mV]")
plt.xlabel("Temperatur [K]")
plt.tick_params(axis='both', which='both', direction='in', length=4, width=2,
               top=True, bottom=True, left=True, right=True)
plt.axvline(x=2.17,linestyle='dotted',color='black')
plt.text(2.2,0.04,'T$_\lambda=2.17\,K$')
plt.grid(linestyle='dotted')
plt.legend()
plt.savefig("out/Calibration.png", dpi=300, bbox_inches='tight', pad_inches=0.0)
plt.show()
#U0=0.00432
#C=4.84
#d=-0.00434

def AllanBradleyToTemp(U,isAboveLambda):
    if isAboveLambda:
        up = CErrAbove/np.log((U-dErrAbove)/U0ErrAbove)
        down = CErrAboveBelow/np.log((U-dErrAboveBelow)/U0ErrAboveBelow)
        uperror = up-C/np.log((U-d)/U0)
        downerror = C/np.log((U-d)/U0)-down
        return C/np.log((U-d)/U0),uperror,downerror
    else:
        up = CErrBelow/C/np.log((U-dErrBelow)/U0ErrBelow)
        down = CErrBelowBelow/C/np.log((U-dErrBelowBelow)/U0ErrBelowBelow)
        uperror = up-CBel/np.log((U-dBel)/U0Bel)
        downerror = CBel/np.log((U-dBel)/U0Bel) - down
        return CBel/np.log((U-dBel)/U0Bel),uperror,downerror








