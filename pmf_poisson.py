"""PMF of Poisson distribution: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

fig, axes = plt.subplots( 2, 2, figsize=([12,7]) )
fig.subplots_adjust( hspace=0.3, wspace=0.3 )

n = np.arange( 0, 21 )

# four choices of parameter nu
nu = [ 0.5, 5.0, 2.0, 10.0 ]

# loop over four sub plots and four nu values in one go using zip
for ax, par in zip( axes.flatten(), nu ):
	pois = poisson.pmf( n, par )
	ax.bar( n, pois )
	ax.text( 17.5, 0.95*pois.max(), r"$\nu=%3.1f$" % par )
	ax.set_xlabel( "$n$")
	ax.set_ylabel( r"$P(n;\nu)$")

plt.savefig( "pmf_poisson.pdf" )
plt.show()

