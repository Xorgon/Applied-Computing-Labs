import numpy as np

xfoil_path = "C:/Users/Elijah/Documents/XFoil/"
w_array = np.linspace(0.6, 1.2, 11)
a = 340.3  # Speed of sound
v = 12.5  # Velocity
M = v / a  # Mach number
nu = 0.00001461  # Kinematic viscosity
L = 0.698  # Chord length of aircraft wing
Re = v * L / nu  # Reynold's number
