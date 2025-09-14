"""Example: dealing with parameter-dependent uncertainties in kafe2"""

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
lin_modell_pars = [ 1.0, 0.3 ]

#  relative uncertainties on y values (assuming x values do not have uncertainties)
ey_rel = 0.3

# generate synthetic data according to linear model
xtrue, ytrue, ydata = generateXYdata( xdata, lin_model, 0., 0., srely=ey_rel, mpar=lin_modell_pars )

# manipulate one data point to exaggerate the effect
ydata[3]=0.5

# compute absolute uncertainties of generated data points
ey = ey_rel * ydata

# now iterate (niter times, until uncertainty stabilizes), replacing y uncertainty by result from previous fit
niter = 5
for i in np.arange( niter ):

	# fit model to data and obtain fit parameters
	result = xy_fit( lin_model, xdata, ydata, y_error=ey, save=False )
	plot( x_label="x", y_label="y", save=False )
	par = result['fit'].parameter_values

	# update uncertainties with those from fit
	ey = ey_rel * lin_model( xdata, *par )	
	print( par )
