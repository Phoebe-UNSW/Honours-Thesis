#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:46:06 2024

@author: phoebe
"""

import random
from matplotlib import pyplot as plt
#%%

# Step 1: Create a coordinate square of size n x n
def create_coordinate_cube(n, m, p):
    cube = [(x, y, z) for x in range(n) for y in range(m) for z in range(p)]
    return cube

# Step 2: Define the search function
def search_coordinate(cube, target):
    for coord in cube:
        if coord == target:
            return f"Coordinate {target} found at index {cube.index(coord)}"
    return f"Coordinate {target} not found in the cube"
#%%

# Usage
n = 21  # This will create a 5x5 square
m = 31
p = 11
coordinate_cube = create_coordinate_cube(n, m, p)
target_coordinate = (random.randint(0, n-1), random.randint(0, m-1), random.randint(0, p-1))

# Search for the coordinate
result = search_coordinate(coordinate_cube, target_coordinate)
print(result)

#%%

# Step 3: Plot the coordinate square and highlight the target coordinate
x_coords, y_coords, z_coords = zip(*coordinate_cube)  # Separate x and y values

fig1 = plt.figure(1)
ax = fig1.add_subplot(projection='3d')
ax.scatter(x_coords, y_coords, z_coords, s=0.5, color='blue', label='Coordinates')
ax.scatter(*target_coordinate, color='red', s=50, label='Target Coordinate')

plt.xlabel('x Coordinate')
plt.ylabel('y Coordinate')
plt.ylabel('z Coordinate')
plt.title('Coordinate Square with Target Highlighted')
plt.legend()

