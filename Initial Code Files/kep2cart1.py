#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 19:36:30 2024

@author: phoebe
"""

import numpy as np
import math
#%%

def kepler_2_Cartesian(w, i, Omega):
    kep2cart_matrix = np.matrix([[math.cos(w), math.sin(w), 0], 
                                 [-math.sin(w), math.cos(w), 0], 
                                 [0, 0, 1]]) * np.matrix([[1, 0, 0], 
                                                          [0, math.cos(i), math.sin(i)], 
                                                          [0, -math.sin(i), math.cos(i)]]) * np.matrix([[math.cos(Omega), math.sin(Omega), 0], 
                                                                                       [-math.sin(Omega), math.cos(Omega), 0], 
                                                                                       [0, 0, 1]])
    pose_cart = kep2cart_matrix
    return pose_cart

w = 132
i = 97.8
Omega = 285

test = kepler_2_Cartesian(w, i, Omega)