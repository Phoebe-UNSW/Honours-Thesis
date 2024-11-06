#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 15:20:34 2024

@author: phoebe
"""
import random

# Step 1: Create a coordinate square of size n x n
def create_coordinate_square(n):
    square = [(x, y) for x in range(n) for y in range(n)]
    return square

# Step 2: Define the search function
def search_coordinate(square, target):
    for coord in square:
        if coord == target:
            return f"Coordinate {target} found at index {square.index(coord)}"
    return f"Coordinate {target} not found in the square"

# Usage
n = 21  # This will create a 5x5 square
coordinate_square = create_coordinate_square(n)
target_coordinate = (random.randint(0, n-1), random.randint(0, n-1))

# Search for the coordinate
result = search_coordinate(coordinate_square, target_coordinate)
print(result)
