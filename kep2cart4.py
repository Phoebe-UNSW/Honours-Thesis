#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 08:16:31 2024

@author: phoebe
"""

import numpy as np
import math
import random
from matplotlib import pyplot as plt

#%% Define functions for conversion from Keplerian to Cartesian coordinates
def kep2cart(alt, ecc, nu, inc, w, RAAN, t):
    # CONSTANTS
    mu_moon = 4902.8001  # km^3/s^2
    rm = 1737.4  # km (mean radius of the moon)
    
    a = alt + rm
    p = a * (1 - ecc**2)
    r_0 = p / (1 + ecc * np.cos(nu))
    
    # Coordinates in the perifocal reference system Oxyz
    x = r_0 * np.cos(nu)
    y = r_0 * np.sin(nu)
    
    Vx_ = -(mu_moon/p)**0.5 * np.sin(nu)
    Vy_ = (mu_moon/p)**0.5 * (ecc + np.cos(nu))
    
    # Convert to the geocentric-equatorial reference system OXYZ
    X = (np.cos(RAAN) * np.cos(w) - np.sin(RAAN) * np.sin(w) * np.cos(inc)) * x + \
        (-np.cos(RAAN) * np.sin(w) - np.sin(RAAN) * np.cos(w) * np.cos(inc)) * y
    Y = (np.sin(RAAN) * np.cos(w) + np.cos(RAAN) * np.sin(w) * np.cos(inc)) * x + \
        (-np.sin(RAAN) * np.sin(w) + np.cos(RAAN) * np.cos(w) * np.cos(inc)) * y
    Z = (np.sin(w) * np.sin(inc)) * x + (np.cos(w) * np.sin(inc)) * y
    
    Vx = (np.cos(RAAN) * np.cos(w) - np.sin(RAAN) * np.sin(w) * np.cos(inc)) * Vx_ + \
         (-np.cos(RAAN) * np.sin(w) - np.sin(RAAN) * np.cos(w) * np.cos(inc)) * Vy_
    Vy = (np.sin(RAAN) * np.cos(w) + np.cos(RAAN) * np.sin(w) * np.cos(inc)) * Vx_ + \
         (-np.sin(RAAN) * np.sin(w) + np.cos(RAAN) * np.cos(w) * np.cos(inc)) * Vy_
    Vz = (np.sin(w) * np.sin(inc)) * Vx_ + (np.cos(w) * np.sin(inc)) * Vy_
    
    X2 = np.rint(X + Vx * t)
    Y2 = np.rint(Y + Vy * t)
    Z2 = np.rint(Z + Vz * t)
    
    return [X2, Y2, Z2]

#%% Usage example with more practical plotting
alt = 50
ecc = 0
inc = math.pi / 2
w = 0
RAAN = 0
t = 180

# Perturb the eccentricity slightly
ecc_pert = ecc + random.randint(0, 9) / 10

# Calculate expected and perturbed positions
pose_expect = kep2cart(alt, ecc, 0, inc, w, RAAN, t)
pose_pert = kep2cart(alt, ecc_pert, 0, inc, w, RAAN, t)

#%% Plot the expected and perturbed positions
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Plot perturbed position
ax.scatter(*pose_pert, color='red', s=50, label='Perturbed Position')

# Plot expected position
ax.scatter(*pose_expect, color='green', s=50, label='Expected Position')

# Set labels and title
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')
plt.title('Expected vs Perturbed Satellite Position')
plt.legend()
plt.show()
