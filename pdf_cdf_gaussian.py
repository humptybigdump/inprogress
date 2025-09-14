"""PDF and CDF of normal (Gaussian) distribution: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#  x values within 0.1% and 99.9% percentiles
x = np.linspace( norm.ppf(0.001), norm.ppf(0.999), 200 )
pdf = norm.pdf( x )
cdf = norm.cdf( x )

fig, ax = plt.subplots( 2, 1, figsize=([7,10]) )

ax[0].plot( x, pdf )
ax[0].set_xlabel( "$x$")
ax[0].set_ylabel( "Probability Density Function" )

ax[1].plot( x, cdf )
ax[1].set_xlabel( "$x$")
ax[1].set_ylabel( "Cumulative Distribution Function" )

plt.savefig( "pdf_cdf_gaussian.pdf" )
plt.show()