#!/usr/bin/env python#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""Using kafe2 interface of PhyPraKit for straight line fit in the laboratory"""

import numpy as np
import matplotlib.pyplot as plt 
from PhyPraKit import generateXYdata, k2Fit
from scipy.optimize import curve_fit
from scipy.stats import chi2

# range of values
n = 3
xdata  = np.array( [ 1.0, 2.0, 3.0 ] )
ydata  = np.array( [ 1.5, 3.6, 4.1 ] )
ey     = np.array( [ 0.5, 0.8, 0.3 ] )

def lin_model( x, a0=1., a1=1. ):
	'''linear model (straight line)'''
	return a0 + a1*x
	
	
# straight line fit using kafe2
par, pare, corr, S = k2Fit( lin_model, xdata, ydata, sy=ey )
ndof = n - len( par )
print( "Results before transformation of variable")
print( "Parameters:    ", par )
print( "Uncertainties: ", pare )
print( "Correlation matrix:\n", corr )
print( "chi2, ndof, chi2/ndof: ", S, ndof, S/ndof )


# transformation of variable: subtract average from all data points
w = 1./ey**2
xtrans = xdata - np.average( xdata, weights=w )

# fit again after transformation
par, pare, corr, S = k2Fit( lin_model, xtrans, ydata, sy=ey )
ndof = n - len( par )
print( "Results after transformation of variable")
print( "Parameters:    ", par )
print( "Uncertainties: ", pare )
print( "Correlation matrix:\n", corr )
print( "chi2, ndof, chi2/ndof: ", S, ndof, S/ndof )



