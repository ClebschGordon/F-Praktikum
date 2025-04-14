import math

import numpy
import numpy as np
import io
import matplotlib.pyplot as plt
from matplotlib import ticker

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
maxVal = voltage[750:].max()
minVal = voltage[750]
readingVal = (maxVal+minVal)/2

fig,ax = plt.subplots()
def plotErrorBars(rangelow,rangehigh):
    plt.plot(AllanBradleyToTemp(AllanBradley[rangelow:rangehigh],True)[0],voltage[rangelow:rangehigh],label='Messwerte')
    #plt.scatter(AllanBradleyToTemp(AllanBradley[750:1300],True)[0]+AllanBradleyToTemp(AllanBradley[750:1300],True)[1],voltage[750:1300])
    #plt.scatter(AllanBradleyToTemp(AllanBradley[750:1300],True)[0]-AllanBradleyToTemp(AllanBradley[750:1300],True)[2],voltage[750:1300])
    xRight = AllanBradleyToTemp(AllanBradley[rangelow:rangehigh],True)[0]+AllanBradleyToTemp(AllanBradley[rangelow:rangehigh],True)[1]
    lowAditional = np.linspace(3.68,xRight.min(),100)
    yRight = voltage[rangelow:rangehigh]
    yAditional = np.linspace(minVal,minVal,100)
    plotPointsX = np.append(lowAditional,xRight)
    plotPointsY = np.append(yAditional,yRight)
    #plt.plot(plotPointsX,plotPointsY,color='black')

    xLeft = AllanBradleyToTemp(AllanBradley[rangelow:rangehigh],True)[0]-AllanBradleyToTemp(AllanBradley[rangelow:rangehigh],True)[2]
    highAditional = np.linspace(xLeft.max(),3.77,100)
    yLeft = voltage[rangelow:rangehigh]
    highAditionalY = np.linspace(maxVal,maxVal,100)
    leftpointsX = np.append(xLeft,highAditional)
    leftpointsY = np.append(yLeft,highAditionalY)
    #plt.plot(leftpointsX,leftpointsY,color='black')

    y2_interp = np.interp(plotPointsX, leftpointsX, leftpointsY)
    plt.fill_between(plotPointsX,plotPointsY,y2_interp,alpha=0.3,label='Fehlerintervall')

plotErrorBars(750,1300)
plotErrorBars(1500,-1)
plt.errorbar(AllanBradleyToTemp(AllanBradley[1300:1500:3],True)[0],voltage[1300:1500:3],voltage[1300:1500:3]*0.05+0.000002,0,label='U$_{Probe}$-Fehlerbehaftete\n Messwerte',zorder=0)
#plt.errorbar(AllanBradleyToTemp(AllanBradley[1500:],True)[0],voltage[1500:],xerr=AllanBradleyToTemp(AllanBradley[1500:],True)[1],yerr=0)
plt.xlim(3.657,3.825)

#plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x * 100:.0}"))
ticks = [0.00008,0.00010,0.00012,0.00014,0.00016,0.00018]
ax.set_yticks(ticks)
labels = ["0.08","0.10","0.12","0.14","0.16","0.18"]
ax.set_yticklabels(labels)
plt.tick_params(axis='both', which='both', direction='in', length=4, width=2,
               top=True, bottom=True, left=True, right=True)
plt.axhline((maxVal+minVal)/2,0.2,0.7,color='black')
plt.axhline(maxVal,0.6,1,color='black')
plt.axhline(minVal,0,0.35,color='black')
plt.axvline(3.731,linestyle='dashed',color = 'black',lw=1)
plt.text(3.7315,0.000072,'T$_c=3.731$')
plt.text(3.769,readingVal+readingVal*0.01,'Mittlere Ausgleichsgerade',size=7)
plt.grid(linestyle='dotted')
plt.xlabel('Temperatur [K]')
plt.ylabel('Spannnung $U_{Probe}\,[\mu V]$')
plt.savefig("out/DirectMeasurement.png", dpi=300, bbox_inches='tight', pad_inches=0.00)
#plt.show()
ValueList = []
for idx,e in enumerate(voltage[750:]):
    if(np.abs(e-readingVal)<=0.0005*math.pow(10,-3)):
        #print(idx+750,AllanBradleyToTemp(AllanBradley[idx+750],True)[0])
        ValueList.append(AllanBradleyToTemp(AllanBradley[idx+750],True)[0])
        #plt.scatter(AllanBradleyToTemp(AllanBradley[idx+750],True)[0],e,color='black',s=15,zorder=3)

Values = np.array(ValueList)

manuallPoints = np.array([3.7239,3.7335,3.7352])
print(np.mean(manuallPoints),np.sqrt(np.var(manuallPoints,ddof=1)))
plt.scatter(manuallPoints[0],readingVal,color='black',zorder=3,marker='.',label='Schnittpunkte')
plt.scatter(manuallPoints[1],readingVal,color='black',zorder=3,marker='.')
plt.scatter(manuallPoints[2],readingVal,color='black',zorder=3,marker='.')

for idx,e in enumerate(AllanBradleyToTemp(AllanBradley[750:],True)[0]):
    if np.abs(e-np.mean(manuallPoints))<=0.00005:print(e,idx)
print(AllanBradleyToTemp(AllanBradley[1755+750],True)[0],AllanBradleyToTemp(AllanBradley[1755+750],True)[1],AllanBradleyToTemp(AllanBradley[1755+750],True)[2])

plt.legend(loc='lower right', fontsize='small')
plt.savefig("out/TCrit.png", dpi=300, bbox_inches='tight', pad_inches=0.01)
plt.show()


