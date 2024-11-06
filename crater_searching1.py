#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 08:34:28 2024

@author: phoebe
"""

import random
import numpy as np
import pandas as pd
#%%

# Define a placeholder crater data structure
class Crater:
    def __init__(self, coord, diameter, depth, albedo):
        self.coord = coord
        self.diameter = diameter  # in km, example characteristic
        self.depth = depth        # in km, example characteristic
        self.albedo = albedo      # reflectivity, example characteristic

    def __repr__(self):
        return f"Crater(coord={self.coord}, diameter={self.diameter}, depth={self.depth}, albedo={self.albedo})"

# Function to generate random crater characteristics for a known coordinate
def generate_crater_for_known_coord(coord):
    diameter = random.uniform(0.5, 10)  # example diameter range in km
    depth = random.uniform(0.1, 2)      # example depth range in km
    albedo = random.uniform(0.1, 0.9)   # reflectivity between 0 and 1
    return Crater(coord, diameter, depth, albedo)

# Create a database with known coordinates and random characteristics
def create_crater_database_with_known_coords(coords):
    return [generate_crater_for_known_coord(coord) for coord in coords]

# Function to find a crater by a given coordinate
def find_crater_by_coordinate(database, target_coord):
    for crater in database:
        if crater.coord == target_coord:
            return crater
    return None

def search_craters(database, min_diameter=None, max_diameter=None, min_depth=None, max_depth=None, albedo_range=None):
    results = []
    for crater in database:
        if (min_diameter is None or crater.diameter >= min_diameter) and \
           (max_diameter is None or crater.diameter <= max_diameter) and \
           (min_depth is None or crater.depth >= min_depth) and \
           (max_depth is None or crater.depth <= max_depth) and \
           (albedo_range is None or albedo_range[0] <= crater.albedo <= albedo_range[1]):
            results.append(crater)
    return results

# Generate a range of known coordinates
def generate_known_coordinates(x_range, y_range, z_range):
    coords = [(x, y, z) for x in range(x_range[0], x_range[1] + 1) 
                            for y in range(y_range[0], y_range[1] + 1) 
                            for z in range(z_range[0], z_range[1] + 1)]
    return coords

# Define the range for coordinates
x_range = (0, 50)  # x coordinates from 0 to 5
y_range = (0, 70)  # y coordinates from 0 to 5
z_range = (0, 40)  # z coordinates from 0 to 5

# Generate known coordinates within the specified ranges
known_coords = generate_known_coordinates(x_range, y_range, z_range)

# Create the crater database using the known coordinates
crater_database = create_crater_database_with_known_coords(known_coords)

# Example usage: Search for a crater at a known coordinate
#target_coord = (25, 50, 20)
target_coord = (
    random.randint(x_range[0], x_range[1]),
    random.randint(y_range[0], y_range[1]),
    random.randint(z_range[0], z_range[1])
)  # Pick a coordinate from the generated coordinates
found_crater = find_crater_by_coordinate(crater_database, target_coord)

# Check if a crater was found and display the result
if found_crater:
    print("Crater found:", found_crater)
else:
    print("No crater found at the given coordinate.")
#%%  

# Create a DataFrame from the crater database
crater_data = pd.DataFrame([{'coord': crater.coord, 'diameter': crater.diameter, 
                             'depth': crater.depth, 'albedo': crater.albedo}
                            for crater in crater_database])

# Function to find a crater by coordinate and access its details
def find_crater_info_by_coord(crater_data, target_coord):
    # Search for the row that matches the target coordinate
    crater_info = crater_data[crater_data['coord'] == target_coord]
    
    if not crater_info.empty:
        # Extract crater attributes
        diameter = crater_info['diameter'].values[0]
        depth = crater_info['depth'].values[0]
        albedo = crater_info['albedo'].values[0]
        
        return diameter, depth, albedo
    else:
        return None

# Example usage

crater_details = find_crater_info_by_coord(crater_data, target_coord)

if crater_details:
    diameter, depth, albedo = crater_details
    print(f"Diameter: {diameter}, Depth: {depth}, Albedo: {albedo}")
else:
    print("No crater found at the given coordinate.")

#%%
epsilon = 0.01 # error percentage

min_diameter = diameter - epsilon * diameter
max_diameter = diameter + epsilon * diameter
min_depth = depth - epsilon * depth
max_depth = depth + epsilon * depth
albedo_min = albedo - epsilon * albedo
albedo_max = albedo + epsilon * albedo
albedo_range = (albedo_min, albedo_max)

# Perform the search
found_pose = search_craters(crater_database, min_diameter=min_diameter, max_diameter=max_diameter, min_depth=min_depth, max_depth=max_depth, albedo_range=albedo_range)

# Check if results were found and handle cases where no matches are found
if not found_pose:
    print("No craters match the given criteria.")
else:
    print("Matching craters found:", found_pose)
