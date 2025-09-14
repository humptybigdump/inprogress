"""Maximum likelihood method: negative log likelihood for more and more data"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# construct negative log likelihood function for Gaussian
def NLL_gaussian( mu, sigma, data ):

    sig2 = sigma**2

    # constant terms ignored as they are irrelevant for the function's minimum
    #N = len( data )
    #const = 0.5 * N * ( np.log(2*np.pi) + np.log( sig2 ) )

    # construct negative log likelihood the Python/NumPy way
    DATA, MU = np.meshgrid( data, mu )
    return np.sum( 0.5*(DATA-MU)**2/sig2, axis=1 )

    # this is equivalent to, but less readable than, the following
    #NLL = 0
    #for i in np.arange( N ):
    #    NLL += 0.5*(data[i]-mu)**2/sig2
    # return NLL

# true model parameters
atrue = 5
sig   = 1

# data points
n = 5
steps = 500
xi = np.linspace( 1, n, n )
xrange = np.linspace( 0.5, n + 0.5, steps )

# scan of a values
mumin, mumax = 0., 10.
mu = np.linspace( mumin, mumax, steps )

rng = np.random.default_rng( 42 )
yi = rng.normal( loc=atrue, scale=sig, size=n )

fig,ax = plt.subplots( 2, 5, figsize=(30,10) )

for i in np.arange( len(yi) ):
    # compute NLL for first i data points
    NLL = NLL_gaussian( mu, sig, yi[:i+1] )

    NLL_min = np.amin( NLL )
    muhat = np.mean( yi[:i+1] ) # using our knowledge that the ML estimator is the mean

    # plot data points
    ax[0][i].errorbar( xi[:i+1], yi[:i+1], yerr=sig, fmt="ro" )
    ax[0][i].set_xlabel( r"$x$")
    ax[0][i].set_ylabel( r"$y$")
    ax[0][i].set_xlim( 0, 6 )
    ax[0][i].set_ylim( 0, 8 )
    ymean = np.repeat( muhat, steps )
    ax[0][i].plot( xrange, ymean, "r--" )

    # plot NLL
    ax[1][i].set_title( r"%d random number(s): $\hat{\mu} = %4.3f$" % ( i+1, muhat ) )
    ax[1][i].plot( mu, NLL-NLL_min )
    ax[1][i].set_xlabel( r"$\mu$")
    ax[1][i].set_ylabel( r"$\Delta(-\ln L(\mu))$")
    ax[1][i].set_xlim( 0, 10 )
    ax[1][i].set_ylim( 0, 50 )

plt.savefig( "ml_gaussian.pdf" )
plt.show()