#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:23:06 2024

@author: phoebe
"""

from astropy.constants import G, M_earth, R_earth
from astropy import units as u
import numpy as np

mu = G.value*M_earth.value
Re = R_earth.value
t = 0

def kep_2_cart(a,e,i,w,Omega,T, EA):

    #1
    M = (t - T)*np.sqrt(mu/(a**3))
    MA = EA - e*np.sin(EA)
    nu = 2*np.arctan(np.sqrt((1+e)/(1-e)) * np.tan(EA/2))
    r = a*(1 - e*np.cos(EA))
    h = np.sqrt(mu*a * (1 - e**2))
    
    X = r*(np.cos(Omega)*np.cos(w+nu) - np.sin(Omega)*np.sin(w+nu)*np.cos(i))
    Y = r*(np.sin(Omega)*np.cos(w+nu) + np.cos(Omega)*np.sin(w+nu)*np.cos(i))
    Z = r*(np.sin(i)*np.sin(w+nu))
    
    p = a*(1-e**2)

    V_X = (X*h*e/(r*p))*np.sin(nu) - (h/r)*(np.cos(Omega)*np.sin(w+nu) + \
    np.sin(Omega)*np.cos(w+nu)*np.cos(i))
    V_Y = (Y*h*e/(r*p))*np.sin(nu) - (h/r)*(np.sin(Omega)*np.sin(w+nu) - \
    np.cos(Omega)*np.cos(w+nu)*np.cos(i))
    V_Z = (Z*h*e/(r*p))*np.sin(nu) + (h/r)*(np.cos(w+nu)*np.sin(i))

    return [X,Y,Z],[V_X,V_Y,V_Z]