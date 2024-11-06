#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:50:02 2024

@author: phoebe
"""

import random
import numpy as np
#%%

# Define a placeholder crater data structure
class Crater:
    def __init__(self, coord, diameter, depth, albedo):
        self.coord = coord
        self.diameter = diameter  # in km, example characteristic
        self.depth = depth        # in km, example characteristic
        self.albedo = albedo      # reflectivity, example characteristic

# Function to generate random crater characteristics
def generate_random_crater(coord_range):
    coord = (random.randint(0, coord_range), random.randint(0, coord_range), random.randint(0, coord_range))
    diameter = random.uniform(0.5, 10)  # example diameter range in km
    depth = random.uniform(0.1, 2)      # example depth range in km
    albedo = random.uniform(0.1, 0.9)   # reflectivity between 0 and 1
    return Crater(coord, diameter, depth, albedo)

# Generate a mock database of craters
def create_crater_database(num_craters, coord_range):
    return [generate_random_crater(coord_range) for _ in range(num_craters)]
#%%
def find_crater_by_coordinate(database, target_coord):
    # Iterate through each crater in the database
    for crater in database:
        # Check if the crater's coordinate matches the target coordinate
        if crater.coord == target_coord:
            return crater  # Return the crater object if a match is found
    return None  # Return None if no match is found

#%%
# Example usage
num_craters = 1000
coord_range = 600
crater_database = create_crater_database(num_craters, coord_range)

# Define the target coordinate
target_coord = (70, 170, 449)

# Call the function to find the crater at the given coordinate
target_crater = find_crater_by_coordinate(crater_database, target_coord)

# Check if a crater was found and display the result
if target_crater:
    print("Crater found:", target_crater)
else:
    print("No crater found at the given coordinate.")
