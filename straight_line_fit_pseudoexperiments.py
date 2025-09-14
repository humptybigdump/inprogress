#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""Using PhyPraKit for a straight line fit in the laboratory course
uncertainties determined from pseudoexperiments (or: toy MC)"""

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

# absolute uncertainty for x value, relative uncertainty for y
ey_rel = 0.1
ex = 0.3

# generate synthetic data according to linear model
xtrue, ytrue, ydata = generateXYdata( xdata, lin_model, ex, 0., srely=ey_rel, mpar=lin_modell_pars )
ey = ey_rel * ytrue 

# or use hard-coded values directly
#xdata = np.array( [ 1.,  2.,  3.,  4. , 5.,  6. , 7.,  8.,  9., 10.] )
#ydata = np.array( [ 1.23912799, 1.59626873, 1.69944363, 1.95397332, 2.26423559, 3.20817472, 3.12755677, 3.09552808, 3.39170581, 4.31564169 ] )
#ey = np.array( [ 0.13, 0.16, 0.19, 0.22, 0.25, 0.28, 0.31, 0.34, 0.37, 0.4 ] )

# pseudoexperiments
rng = np.random.default_rng( 42 )

Npe = 1000
par = np.zeros( (Npe, 2) )

for i in np.arange( Npe ):
	"""New pseudoexperiment: draw random x and y values from Gaussian distribution
	using mu = measured value and sigma = given uncertainty"""
	xpe = rng.normal( size=n, loc=xdata, scale=ex )
	ype = rng.normal( size=n, loc=ydata, scale=ey )
	result = xy_fit( lin_model, xpe, ype, x_error=ex, y_error=ey, save=False )
	par[i] = result['fit'].parameter_values

a0, a1 = par[:,0], par[:,1]
fig,ax = plt.subplots( 2, 2, figsize=(12,10) )

ax[0][0].hist( a0 )
ax[0][0].set_xlabel( r"$a_{0}$" )
ax[0][0].set_ylabel( "Frequency" )
ax[0][0].text(0.66, 0.85, r"$\hat{\mu} = $%5.3f %s$\hat\sigma = $%5.3f" % (np.mean( a0 ), "\n", np.std( a0, ddof=1 ) ), transform=ax[0][0].transAxes, backgroundcolor='white')

ax[1][1].hist( a1 )
ax[1][1].set_xlabel( r"$a_{1}$" )
ax[1][1].set_ylabel( "Frequency" )
ax[1][1].text(0.66, 0.85, r"$\hat{\mu} = $%5.3f %s$\hat\sigma = $%5.3f" % (np.mean( a1 ), "\n", np.std( a1, ddof=1 ) ), transform=ax[1][1].transAxes, backgroundcolor='white')

ax[1][0].scatter( a1, a0 )
ax[1][0].set_xlabel( r"$a_{1}$" )
ax[1][0].set_ylabel( r"$a_{0}$" )
ax[1][0].text(0.66, 0.85, r"$\hat{\rho} = $%5.3f" % np.corrcoef( a1, a0 )[1][0], transform=ax[1][0].transAxes, backgroundcolor='white')

xline = np.linspace( xmin-0.5, xmax+0.5, 200 )
result = xy_fit( lin_model, xtrue, ytrue, x_error=ex, y_error=ey, save=False )

# kafe2 fit returns parameter estimates, e.g. using the fit object
pardata = result['fit'].parameter_values

ax[0][1].errorbar( xdata, ydata, xerr=ex, yerr=ey, fmt='bo' )
ax[0][1].plot( xline, lin_model( xline, *pardata ), 'r--' )
ax[0][1].set_xlabel( r"$x$" )
ax[0][1].set_ylabel( r"$y$" )

# kafe2 fit also returns asymmetric uncertaintties and correlation matrix
parunc  = result['fit'].asymmetric_parameter_errors
parcorr = result['fit'].parameter_cor_mat
ax[1][0].text(0.60, 0.10, r"$a_0 = %5.3f^{+%5.3f}_{%5.3f}$%s$a_1 = %5.3f^{+%5.3f}_{%5.3f}$%s$\rho = %5.3f$" % (pardata[0],parunc[0][1],parunc[0][0],"\n",pardata[1],parunc[1][1],parunc[1][0],"\n",parcorr[1][0]), transform=ax[0][1].transAxes, backgroundcolor='white')

plt.savefig( "straight_line_fit_pseudoexperiments.pdf", bbox_inches='tight')
plt.show()