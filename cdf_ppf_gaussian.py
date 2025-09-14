""" CDF and quantiles of normal (Gaussian) distribution: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# x values within 0.1% and 99.9% percentiles
amin, amax = 0.001, 0.999
x = np.linspace( norm.ppf(amin), norm.ppf(amax), 200 )
cdf = norm.cdf( x )

# alpha values
alpha = np.linspace( amin, amax, 200 )
ppf = norm.ppf( alpha )

fig, ax = plt.subplots( 2, 1, figsize=([7,10]) )

ax[0].plot( x, cdf )
ax[0].set_xlabel( "$x$")
ax[0].set_ylabel( "Cumulative Distribution Function" )

ax[1].plot( alpha, ppf )
ax[1].set_xlabel( r"$\alpha$")
ax[1].set_ylabel( r"Quantiles $x_{\alpha}$" )

# add horizontal and vertical lines at median and 1 standard deviation
quantile = np.array([-1,0,1])
alpha    = norm.cdf( quantile )
ax[1].hlines( quantile, amin, alpha, linestyles='dashed', colors='black')
ax[1].vlines( alpha, norm.ppf(amin), quantile, linestyles='dashed', colors='black')

# add text for values of alpha for 1 standard deviation
for a in alpha:
    ax[1].text( a+0.02, norm.ppf(amin), "%5.3f" % a  )

plt.savefig( "cdf_ppf_gaussian.pdf" )
plt.show()

