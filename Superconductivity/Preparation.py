import math

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def B_field(z, mu0, n, I, r, R, L):
    term1 = (R + np.sqrt(R**2 + (L/2 + z)**2)) / (r + np.sqrt(r**2 + (L/2 + z)**2))
    term2 = (R + np.sqrt(R**2 + (L/2 - z)**2)) / (r + np.sqrt(r**2 + (L/2 - z)**2))
    Bz = (mu0 * n * I / (2*R - 2*r)) * np.log(term1 * term2)
    return Bz

# Define constants
mu0 = 4 * np.pi * 1e-7  # Permeability of free space (T*m/A)
n = 10353/(193*math.pow(10,-3))  # Turns per meter
I = 440*math.pow(10,-3)  # Current in Amperes
r = 10.5*math.pow(10,-3) # Inner radius in meters
R = 20.4*math.pow(10,-3)  # Outer radius in meters
L = 193*math.pow(10,-3)  # Length of the solenoid in meters

# Define z-axis range
z_values = np.linspace(-2*L, 2*L, 500)
B_values = B_field(z_values, mu0, n, I, r, R, L)
BZero = B_field(0,mu0,n,I,r,R,L)

# Plot the magnetic field
plt.figure(figsize=(8, 5))
plt.plot(z_values, B_values, label='B(z)', color='b')
plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
plt.axhline(0, color='black', linestyle='-', linewidth=0.8)
plt.axhline(BZero,label=BZero/I)
plt.xlabel("z (m)")
plt.ylabel("B (T)")
plt.title("Magnetic Field B(z) Inside a Finite Solenoid")
plt.legend()
plt.grid()
plt.show()