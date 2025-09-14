"""CDF of normal distribution and error function: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import erf

# x values within 0.1% and 99.9% percentiles
amin, amax = 0.001, 0.999
x = np.linspace( norm.ppf(amin), norm.ppf(amax), 200 )

fig, ax = plt.subplots( 2, 1, figsize=([7,10]) )

ax[0].plot( x, norm.cdf(x) )
ax[0].set_xlabel( "$x$")
ax[0].set_ylabel( r"$\Phi(x)$" )

ax[1].plot( x, erf(x) )
ax[1].set_xlabel( "$x$")
ax[1].set_ylabel( "erf$(x)$" )

plt.savefig( "cdf_erf_gaussian.pdf" )
plt.show()

