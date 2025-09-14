""""
illustration of a random variable as a mapping 
from probability space to measurement space
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# probability space: true parameters of Gaussian known
true_mu, true_sigma = 0., 1.
 
rng = np.random.default_rng( 42 )
data = rng.normal( true_mu, true_sigma, size=20 )
mu, sig  = np.mean( data ), np.std( data, ddof=1 )
print( "Estimates of mu and sigma: ", mu, sig )

# plot probability density from which measurements were drawn
x = np.linspace( -3, 3, 200 )
pdf = norm.pdf( x, loc=true_mu, scale=true_sigma )

# plot measurements as lines
plt.vlines( data, 0, 0.1, linestyles='-', lw=2)
plt.plot( x, pdf, 'r' )
plt.xlim( -3.3, 3.3 )
plt.ylim( 0, 0.5 )
plt.xlabel( "$x$" )
plt.ylabel( "probability density")

plt.savefig( "random_variable.pdf" )
plt.show()

