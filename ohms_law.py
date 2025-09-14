"""Using PhyPraKit for a straight line fit in the laboratory course: Ohm's law as an example"""

import numpy as np
import matplotlib.pyplot as plt 
import kafe2
from PhyPraKit import k2Fit

def ohm_model_G( V, G=1. ):
	'''Ohm's Law using conductance'''
	return G*V

def ohm_model_R( V, R=1. ):
	'''Ohm's Law using resistance'''
	return V/R

def lin_model( V, G=1., I0=0. ):
	'''linear model (straight line)'''
	return G*V + I0
	
# absolute uncertainties in x and y
ex, ey = 0.015, 0.015

# read data from CSV file
data = np.genfromtxt('DataOhmsLaw.csv', delimiter=",", skip_header=3 )
V, I = data[:,0], data[:,1]
labels = [ r"$V$ (V)", r"$I$ (A)" ]

# straight line fit: use kafe2 wrapper function xy_fit() for fitting and plot() plotting
# Note: without setting save=False, a file with fit results would be saved

# fit to Ohm's law with conductance G
result_ohm_G = kafe2.xy_fit( ohm_model_G, V, I, x_error=ex, y_error=ey, save=False )
kafe2.plot( x_label=labels[0], y_label=labels[1], save=False )

# fit to Ohm's law with resistance R
result_ohm_R = kafe2.xy_fit( ohm_model_R, V, I, x_error=ex, y_error=ey, save=False )
kafe2.plot( x_label=labels[0], y_label=labels[1], save=False )

# fit to linear model with additional current I0
result_lin = kafe2.xy_fit( lin_model, V, I, x_error=ex, y_error=ey, save=False )
kafe2.plot( x_label=labels[0], y_label=labels[1], save=False )
print( result_lin )

# legacy code for backwards compatibility using PhyPraKit.k2Fit()
#par, pare, corr, S = k2Fit( ohm_model_G, V, I, sx=ex, sy=ey, axis_labels=labels )
#par, pare, corr, S = k2Fit( ohm_model_R, V, I, sx=ex, sy=ey, axis_labels=labels )
#par, pare, corr, S = k2Fit( lin_model, V, I, sx=ex, sy=ey, axis_labels=labels )
#print( par, pare, corr, S )