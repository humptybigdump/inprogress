#!/usr/bin/env python 

# Simulation of measurement using a computer
# U. Husemann, April 2021
# Changes: T. Ferber, April 2022

import numpy as np

# number of measurements
n = 10

# NumPy array of true values
w = 1.0 * np.ones( n )

# Numpy-Array of random contribution, simulated as Gaussian random numbers with a mean value of 0 and a width of 0.1 s^-1
rng = np.random.default_rng( 42 )
z = rng.normal( 0, 0.1, n )

for i in range( n ):
	print( 'w = {:.2f}   m = w + z = {:.2f}'.format( w[i], w[i]+z[i] ) ) 
