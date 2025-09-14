"""PMF of binomial distribution: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

fig, axes = plt.subplots( 2, 2, figsize=([12,7]) )
fig.subplots_adjust( hspace=0.3, wspace=0.3 )

n = np.arange( 0, 11 )

# four sets of parameters N, p for binomial distribution
parameter = [ [5,0.3], [5,0.7], [10,0.3], [10,0.7] ]

# loop over four sub plots and four parameter sets in one go using zip
for ax, par in zip( axes.flatten(), parameter ):
	binomial = binom.pmf( n, par[0], par[1] )
	ax.bar( n, binomial )
	ax.text( 7.8, 0.95*binomial.max(), "$N=%d$, $p=%3.1f$" % ( par[0], par[1] ))
	ax.set_xlabel( "$n$")
	ax.set_ylabel( "$P(n;N,p)$")

plt.savefig( "pmf_binomial.pdf" )
plt.show()

