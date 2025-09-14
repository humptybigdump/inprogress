"""Using PhyPraKit for a straight line fit in the laboratory course: dealing with x and y uncertainties"""

import numpy as np
import matplotlib.pyplot as plt 
from PhyPraKit import generateXYdata
from kafe2 import xy_fit, plot

# range of values
n, xmin, xmax = 10, 1., 10.
xdata = np.linspace( xmin, xmax, n )

def lin_model( x, a0=1., a1=1. ):
	'''linear model (straight line)'''
	return a0 + a1*x

# true parameter values
lin_model_pars  = [ 1.0, 0.3 ]

# absolute uncertainty on x values, relative uncertainty on y
ey_rel = 0.1
ex = 0.3

# correlated uncertainties in both x and y
xcorr, ycorr = 0.1, 0.3

# generate synthetic data according to linear model
xtrue, ytrue, ydata = generateXYdata( xdata, lin_model, ex, 0., srely=ey_rel, mpar=lin_model_pars, xrelcor=xcorr, yrelcor=ycorr )
ey = ey_rel * ytrue 

# straight line fit with kafe
result = xy_fit( lin_model, xdata, ydata, x_error=0, y_error=ey, save=False )
plot( x_label="x", y_label="y", save=False )
print( "Linear fit with y uncertainties only")
print( "Parameters:    ", result['fit'].parameter_values )
print( "Uncertainties: ", result['fit'].parameter_errors )
print( "Correlation matrix:\n", result['fit'].parameter_cov_mat )
print( "chi2, ndof, chi2/ndof: ", result['goodness_of_fit'], result['ndf'], result['gof/ndf'] )

# straight line fit with kafe
result = xy_fit( lin_model, xdata, ydata, x_error=ex, y_error=ey, save=False )
plot( x_label="x", y_label="y", save=False )
print( "Linear fit with x and y uncertainties")
print( "Parameters:    ", result['fit'].parameter_values )
print( "Uncertainties: ", result['fit'].parameter_errors )
print( "Correlation matrix:\n", result['fit'].parameter_cov_mat )
print( "chi2, ndof, chi2/ndof: ", result['goodness_of_fit'], result['ndf'], result['gof/ndf'] )