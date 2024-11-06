#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 23:17:46 2024

@author: phoebe
"""

import numpy as np
import math
import random
from matplotlib import pyplot as plt
#%%

def kep2cart(alt, ecc, nu, inc, w, RAAN, t):
    # CONSTANST
    mu_moon = 4902.8001 #km3/s2
    rm = 1737.4 #km
    
    a = alt + rm
    p = a * (1-ecc**2)
    r_0 = p / (1 + ecc * np.cos(nu)) 
    
    # Coordinates in the perifocal reference system Oxyz 
    x = r_0 * np.cos(nu)
    y = r_0 * np.sin(nu)
    
    Vx_ = -(mu_moon/p)**(1/2) * np.sin(nu)
    Vy_ = (mu_moon/p)**(1/2) * (ecc + np.cos(nu))
    
    # the geocentric-equatorial reference system OXYZ
    X = (np.cos(RAAN) * np.cos(w) - np.sin(RAAN) * np.sin(w) * np.cos(inc)) * x + (-np.cos(RAAN) * np.sin(w) - np.sin(RAAN) * np.cos(w) * np.cos(inc)) * y
    Y = (np.sin(RAAN) * np.cos(w) + np.cos(RAAN) * np.sin(w) * np.cos(inc)) * x + (-np.sin(RAAN) * np.sin(w) + np.cos(RAAN) * np.cos(w) * np.cos(inc)) * y
    Z = (np.sin(w) * np.sin(inc)) * x + (np.cos(w) * np.sin(inc)) * y
    
    Vx = (np.cos(RAAN) * np.cos(w) - np.sin(RAAN) * np.sin(w) * np.cos(inc)) * Vx_ + (-np.cos(RAAN) * np.sin(w) - np.sin(RAAN) * np.cos(w) * np.cos(inc)) * Vy_
    Vy = (np.sin(RAAN) * np.cos(w) + np.cos(RAAN) * np.sin(w) * np.cos(inc)) * Vx_ + (-np.sin(RAAN) * np.sin(w) + np.cos(RAAN) * np.cos(w) * np.cos(inc)) * Vy_
    Vz = (np.sin(w) * np.sin(inc)) * Vx_ + (np.cos(w) * np.sin(inc)) * Vy_
    
    X2 = np.rint(X + Vx * t)
    Y2 = np.rint(Y + Vy * t)
    Z2 = np.rint(Z + Vz * t)
    
    return [X2,Y2,Z2]

#%%
def pert_kep2cart(alt, ecc_pert, nu, inc, w, RAAN, t):
    # CONSTANST
    mu_moon = 4902.8001 #km3/s2
    rm = 1737.4 #km
    
    a = alt + rm
    p = a * (1-ecc_pert**2)
    r_0 = p / (1 + ecc_pert * np.cos(nu)) 
    
    # Coordinates in the perifocal reference system Oxyz 
    x = r_0 * np.cos(nu)
    y = r_0 * np.sin(nu)
    
    Vx_ = -(mu_moon/p)**(1/2) * np.sin(nu)
    Vy_ = (mu_moon/p)**(1/2) * (ecc_pert + np.cos(nu))
    
    # the geocentric-equatorial reference system OXYZ
    X = (np.cos(RAAN) * np.cos(w) - np.sin(RAAN) * np.sin(w) * np.cos(inc)) * x + (-np.cos(RAAN) * np.sin(w) - np.sin(RAAN) * np.cos(w) * np.cos(inc)) * y
    Y = (np.sin(RAAN) * np.cos(w) + np.cos(RAAN) * np.sin(w) * np.cos(inc)) * x + (-np.sin(RAAN) * np.sin(w) + np.cos(RAAN) * np.cos(w) * np.cos(inc)) * y
    Z = (np.sin(w) * np.sin(inc)) * x + (np.cos(w) * np.sin(inc)) * y
    
    Vx = (np.cos(RAAN) * np.cos(w) - np.sin(RAAN) * np.sin(w) * np.cos(inc)) * Vx_ + (-np.cos(RAAN) * np.sin(w) - np.sin(RAAN) * np.cos(w) * np.cos(inc)) * Vy_
    Vy = (np.sin(RAAN) * np.cos(w) + np.cos(RAAN) * np.sin(w) * np.cos(inc)) * Vx_ + (-np.sin(RAAN) * np.sin(w) + np.cos(RAAN) * np.cos(w) * np.cos(inc)) * Vy_
    Vz = (np.sin(w) * np.sin(inc)) * Vx_ + (np.cos(w) * np.sin(inc)) * Vy_
    
    X2 = np.rint(X + Vx * t)
    Y2 = np.rint(Y + Vy * t)
    Z2 = np.rint(Z + Vz * t)
    
    
    return [X2,Y2,Z2]

#%%
alt = 50
nu = (0,0,50)
inc = math.pi / 2
ecc = 0
ecc_pert = ecc + random.randint(0, 9) / 10
nu = 0
w = 0
RAAN = 0
t = 180

pose_expect = kep2cart(alt, ecc, nu, inc, w, RAAN, t)

pose_pert = pert_kep2cart(alt, ecc_pert, nu, inc, w, RAAN, t)



#%%

# Step 1: Create a coordinate square of size n x n
def create_coordinate_cube(n, m, p):
    cube = [(x, y, z) for x in range(n) for y in range(m) for z in range(l)]
    return cube

# Step 2: Define the search function
def search_coordinate(cube, target):
    for coord in cube:
        if coord == target:
            return f"Coordinate {target} found at index {cube.index(coord)}"
    return f"Coordinate {target} not found in the cube"
#%%

# Usage
n = 1788 + 100  # This will create a 5x5 square
m = 1788 + 100
l = 1788 + 100
coordinate_cube = create_coordinate_cube(n, m, l)
target_coordinate = (random.randint(0, n-1), random.randint(0, m-1), random.randint(0, l-1))

# Search for the coordinate
result = search_coordinate(coordinate_cube, pose_pert)
print(result)

#%%

# Step 3: Plot the coordinate square and highlight the target coordinate
x_coords, y_coords, z_coords = zip(*coordinate_cube)  # Separate x and y values

fig1 = plt.figure(1)
ax = fig1.add_subplot(projection='3d')
ax.scatter(x_coords, y_coords, z_coords, s=0.1, color='blue', label='Coordinates')
ax.scatter(*pose_pert, color='red', s=50, label='Satellite position')
ax.scatter(*pose_expect, color='red', s=50, label='Expected position')

plt.xlabel('x Coordinate')
plt.ylabel('y Coordinate')
plt.ylabel('z Coordinate')
plt.title('Coordinate Square with Target Highlighted')
plt.legend()



