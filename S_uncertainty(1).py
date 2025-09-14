"""least squares: sum of residuals adding more and more data"""

import numpy as np
import matplotlib.pyplot as plt

def LeastSquares_S( model, sigma, data ):
	"""least squares: function to compute squared sum of residuals"""

	# use np.meshgrid to process arrays of models applied on the same data
	MODEL, DATA = np.meshgrid( model, data )
	return np.sum( ( ( DATA - MODEL ) / sigma )**2, axis=0 )

# true model parameters
atrue = 3
sig   = 1

# scan of a values
amin, amax, steps = 0., 6., 300
a = np.linspace( amin, amax, steps )

# data points
N = 5
xi = np.linspace( 1, N, N )
xrange = np.linspace( 0.5, N + 0.5, steps )

rng = np.random.default_rng( 42 )
yi = rng.normal( loc=atrue, scale=sig, size=N )

fig,ax = plt.subplots( 2, N, figsize=(25,10) )

for i in np.arange( len( yi ) ):

	# compute S(a) with first i+1 data points
	S_plot = LeastSquares_S( a, sig, yi[:i+1] )
	
	# plot data points
	ax[0][i].errorbar( xi[:i+1], yi[:i+1], yerr=sig, fmt="ro" )
	ax[0][i].set_xlabel( r"$x$")
	ax[0][i].set_ylabel( r"$y$")
	ax[0][i].set_xlim( 0, 6 )
	ax[0][i].set_ylim( 0, 6 )
	ymean = np.repeat( np.mean( yi[:i+1] ), steps )
	ax[0][i].plot( xrange, ymean, "r--" )

	# plot S(a)
	ax[1][i].plot( a, S_plot )
	ax[1][i].set_xlabel( r"$a$")
	ax[1][i].set_ylabel( r"$S(a)$")
	ax[1][i].set_xlim( 0, 6 )
	ax[1][i].set_ylim( 0, 50 )
	ax[1][i].text( 0.5, 45, "$N=%d$" % (i+1) )

plt.savefig( "S_uncertainty.pdf" )
plt.show()
