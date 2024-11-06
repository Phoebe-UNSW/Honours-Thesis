#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 08:22:08 2024

@author: phoebe
"""

import numpy as np
import math
import random
from matplotlib import pyplot as plt

# Define the function to calculate Cartesian coordinates
def kep2cart(alt, ecc, nu, inc, w, RAAN, t):
    mu_moon = 4902.8001  # km^3/s^2
    rm = 1737.4  # km (mean radius of the moon)
    
    a = alt + rm
    p = a * (1 - ecc**2)
    r_0 = p / (1 + ecc * np.cos(nu))
    
    # Coordinates in the perifocal reference system Oxyz
    x = r_0 * np.cos(nu)
    y = r_0 * np.sin(nu)
    
    Vx_ = -(mu_moon / p) ** 0.5 * np.sin(nu)
    Vy_ = (mu_moon / p) ** 0.5 * (ecc + np.cos(nu))
    
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

# Parameters for expected and perturbed satellite positions
alt = 50
ecc = 0
inc = math.pi / 2
w = 0
RAAN = 0
t = 180

# Generate expected and perturbed positions
pose_expect = kep2cart(alt, ecc, 0, inc, w, RAAN, t)
ecc_pert = ecc + random.randint(0, 9) / 10
pose_pert = kep2cart(alt, ecc_pert, 0, inc, w, RAAN, t)

# Define the search box region around the expected position
box_size = 50  # Distance range to check around the expected position

def is_within_box(position, reference, box_size):
    """Check if the position is within a box centered around the reference point with given box size."""
    return all(abs(position[i] - reference[i]) <= box_size for i in range(3))

# Check if the perturbed and expected positions are within the box
found_expected = is_within_box(pose_expect, pose_expect, box_size)
found_perturbed = is_within_box(pose_pert, pose_expect, box_size)

# Print results
print("Expected position found within box:", found_expected)
print("Perturbed position found within box:", found_perturbed)

#%% Plotting
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Plot the expected and perturbed positions
ax.scatter(*pose_expect, color='green', s=50, label='Expected Position')
ax.scatter(*pose_pert, color='red', s=50, label='Perturbed Position')

# Draw the search box (for illustration only, using a single corner and range)
box_x = [pose_expect[0] - box_size, pose_expect[0] + box_size]
box_y = [pose_expect[1] - box_size, pose_expect[1] + box_size]
box_z = [pose_expect[2] - box_size, pose_expect[2] + box_size]
ax.plot([box_x[0], box_x[1]], [box_y[0], box_y[1]], [box_z[0], box_z[1]], color='blue', label='Search Box')

# Labeling
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')
plt.title('Expected and Perturbed Satellite Positions within Search Box')
plt.legend()
plt.show()
