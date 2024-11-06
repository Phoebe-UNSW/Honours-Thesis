#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 23:29:35 2024

@author: phoebe
"""

import random
import numpy as np
import pandas as pd
#%%
epsilon = 0.05 # 5% expected uncertainty in position
# Define the range for coordinates based on the final propagated position
x_range = (int(np.floor(-8.38290668e+02 - (8.38290668e+02 * epsilon))), int(np.ceil(-8.38290668e+02 + (8.38290668e+02 * epsilon))))
y_range = (int(np.floor(-1.50464491e+03 - (1.50464491e+03 * epsilon))), int(np.ceil(-1.50464491e+03 + (1.50464491e+03 * epsilon))))
z_range = (int(np.floor(-5.92665201e+02 - (5.92665201e+02 * epsilon))), int(np.ceil(-5.92665201e+02 + (5.92665201e+02 * epsilon))))

target_coord = (int(np.round(-8.38290944e+02)), int(np.round(-1.50462630e+03)), int(np.round(-5.92711818e+02)))  # Final Real position from SPICE
#%%
# Generate a range of known coordinates
def generate_known_coordinates(x_range, y_range, z_range):
    coords = [(x, y, z) for x in range(x_range[0], x_range[1] + 1) 
                            for y in range(y_range[0], y_range[1] + 1) 
                            for z in range(z_range[0], z_range[1] + 1)]
    return coords
known_coords = generate_known_coordinates(x_range, y_range, z_range)
#%%
# Define a placeholder crater data structure
class Crater:
    def __init__(self, coord, diameter, depth):
        self.coord = coord
        self.diameter = diameter  # in km, example characteristic
        self.depth = depth        # in km, example characteristic

    def __repr__(self):
        return f"Crater(coord={self.coord}, diameter={self.diameter}, depth={self.depth})"

# Function to generate random crater characteristics for a known coordinate
def generate_crater_for_known_coord(coord):
    diameter = random.uniform(0.5, 10)  # example diameter range in km
    depth = random.uniform(0.1, 2)      # example depth range in km
    return Crater(coord, diameter, depth)

# Create a database with known coordinates and random characteristics
def create_crater_database_with_known_coords(coords):
    return [generate_crater_for_known_coord(coord) for coord in coords]

# Create the crater database using the known coordinates
crater_database = create_crater_database_with_known_coords(known_coords)

#%%
# Function to find a crater by a given coordinate
def find_crater_by_coordinate(database, target_coord):
    for crater in database:
        if crater.coord == target_coord:
            return crater
    return None

found_crater = find_crater_by_coordinate(crater_database, target_coord)

# Check if a crater was found and display the result
if found_crater:
    print("Crater found:", found_crater)
else:
    print("No crater found at the given coordinate.")

#%%

# Create a DataFrame from the crater database
crater_data = pd.DataFrame([{'coord': crater.coord, 'diameter': crater.diameter, 
                             'depth': crater.depth}
                            for crater in crater_database])

# Function to find a crater by coordinate and access its details
def find_crater_info_by_coord(crater_data, target_coord):
    # Search for the row that matches the target coordinate
    crater_info = crater_data[crater_data['coord'] == target_coord]
    
    if not crater_info.empty:
        # Extract crater attributes
        diameter = crater_info['diameter'].values[0]
        depth = crater_info['depth'].values[0]
        
        return diameter, depth
    else:
        return None

# Example usage

crater_details = find_crater_info_by_coord(crater_data, target_coord)

if crater_details:
    diameter, depth = crater_details
    print(f"Diameter: {diameter}, Depth: {depth}")
else:
    print("No crater found at the given coordinate.")

#%%
error = 0.005 # error percentage

min_diameter = diameter - error * diameter
max_diameter = diameter + error * diameter
min_depth = depth - error * depth
max_depth = depth + error * depth

def search_craters(database, min_diameter=None, max_diameter=None, min_depth=None, max_depth=None):
    results = []
    for crater in database:
        if (min_diameter is None or crater.diameter >= min_diameter) and \
           (max_diameter is None or crater.diameter <= max_diameter) and \
           (min_depth is None or crater.depth >= min_depth) and \
           (max_depth is None or crater.depth <= max_depth):
            results.append(crater)
    return results

# Perform the search
found_pose = search_craters(crater_database, min_diameter=min_diameter, max_diameter=max_diameter, min_depth=min_depth, max_depth=max_depth)

# Check if results were found and handle cases where no matches are found
if not found_pose:
    print("No craters match the given criteria.")
else:
    print("Matching craters found:", found_pose)