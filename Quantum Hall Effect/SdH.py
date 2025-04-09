import matplotlib.pyplot as plt
import numpy as np
import io
from scipy.fft import fft, fftfreq
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# Daten einlesen und verarbeiten
file_path = "Data_Nick_Salah/3.dat"
with open(file_path, "r") as file:
    processed_text = file.read().replace(",", ".")

data = np.genfromtxt(io.StringIO(processed_text), 
                    skip_header=15,
                    skip_footer=131,
                    delimiter=None,          # Beliebige Leerzeichen als Trennzeichen
                    filling_values=np.nan,   # Fehlende Werte als NaN
                    invalid_raise=False)     # Überspringe fehlerhafte Zeilen

# Spalten extrahieren
time = data[:,0]
B = np.abs(data[:,1]*9/10)  # Betrag des Magnetfelds
U_hall = data[:,2]
U_xx = data[:,4]
I = data[:,3]  # Strom in mA (Annahme: Shunt-Widerstand = 1 Ohm)

# Widerstände berechnen
rho_xx = U_xx/I *200*10**(-6)/(1.2*10**(-3))*5000
rho_xy = U_hall/I *5000 

# 1/B mit Filterung für endliche Werte
inv_B = 1/B[B != 0]
rho_xx_filtered = rho_xx[B != 0]

# Sortieren der Daten
sort_idx = np.argsort(inv_B)
inv_B_sorted = inv_B[sort_idx]
rho_xx_sorted = rho_xx_filtered[sort_idx]

# Interpolation auf äquidistantes 1/B-Gitter
n_points = 150000
inv_B_interp = np.linspace(inv_B_sorted.min(), inv_B_sorted.max(), n_points)
f = interp1d(inv_B_sorted, rho_xx_sorted, kind='linear')
rho_xx_interp = f(inv_B_interp)

# Glättung und Differentiation
drho_xx = np.gradient(rho_xx_interp, inv_B_interp)

# Fourier-Transformation
N = len(inv_B_interp)
T = np.mean(np.diff(inv_B_interp))

yf = fft(drho_xx)
xf = fftfreq(N, T)[:N//2]

# Hauptfrequenz finden
main_freq = xf[np.argmax(np.abs(yf[0:N//2]))]
delta_inv_B = 1/main_freq

# Trägerdichte berechnen
e = 1.602e-19  # Elementarladung
h = 6.626e-34   # Planck-Konstante
n = e/(h* delta_inv_B )

# Plots
plt.figure(figsize=(12, 8))

# Plot 1: Rho_xx über 1/B
plt.subplot(2, 1, 1)
plt.plot(inv_B_sorted, rho_xx_sorted, label='Original')
plt.plot(inv_B_interp, rho_xx_interp, label='Interpoliert & geglättet')
plt.xlabel('1/B (1/T)')
plt.ylabel('$\\rho_{xx}$ (Ω)')
plt.title('Shubnikov-de-Haas-Oszillationen')
plt.grid(True)
plt.legend()

# Plot 2: FFT-Spektrum
plt.subplot(2, 1, 2)
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.xlabel('Frequenz (1/(1/T))')
plt.ylabel('Amplitude')
plt.title(f'Fourier-Spektrum - Hauptfrequenz: {main_freq:.2f} 1/(1/T)')
plt.annotate(f'$Δ(1/B) = {delta_inv_B:.4f}$ 1/T\n$n = {n/1e15:.2f}×10^{{15}}$ m$^{{-2}}$', 
             xy=(0.7, 0.8), xycoords='axes fraction')
plt.grid(True)

plt.tight_layout()
plt.show()
