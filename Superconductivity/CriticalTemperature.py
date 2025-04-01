import math
import numpy as np
import io
import matplotlib.pyplot as plt
file_path = "Nick_Salah/Nick_Sala_SC_25.dat"

# Read file and replace commas with dots in memory
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

# Convert text into a file-like object and load data, skipping headers
data = np.genfromtxt(io.StringIO(processed_text), skip_header=15)

from Supercond_Script import AllanBradleyToTemp
AllanBradley = data[:,3]
voltage = data[:,1]

#plt.plot(AllanBradleyToTemp(AllanBradley[:],True)[0],voltage[:])
#plt.show()
plt.errorbar(AllanBradleyToTemp(AllanBradley[750:1500],True)[0],voltage[750:1500],xerr=AllanBradleyToTemp(AllanBradley[750:1500],True)[1],yerr=0)
plt.errorbar(AllanBradleyToTemp(AllanBradley[1500:],True)[0],voltage[1500:],xerr=AllanBradleyToTemp(AllanBradley[1500:],True)[1],yerr=0)
plt.xlim(3.7,3.77)

maxVal = voltage[750:].max()
minVal = voltage[750]
readingVal = (maxVal+minVal)/2

plt.axhline((maxVal+minVal)/2)
#plt.show()
ValueList = []
for idx,e in enumerate(voltage[750:]):
    if(np.abs(e-readingVal)<=0.0005*math.pow(10,-3)):
        #print(idx+750,AllanBradleyToTemp(AllanBradley[idx+750],True)[0])
        ValueList.append(AllanBradleyToTemp(AllanBradley[idx+750],True)[0])
        #plt.scatter(AllanBradleyToTemp(AllanBradley[idx+750],True)[0],e,color='black',s=15,zorder=3)

Values = np.array(ValueList)

manuallPoints = np.array([3.7239,3.7335,3.7351])
print(np.mean(manuallPoints),np.sqrt(np.var(manuallPoints,ddof=1)))
plt.scatter(manuallPoints[0],readingVal,color='black',zorder=3,marker='x')
plt.scatter(manuallPoints[1],readingVal,color='black',zorder=3,marker='x')
plt.scatter(manuallPoints[2],readingVal,color='black',zorder=3,marker='x')
plt.show()




