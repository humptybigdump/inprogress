"""draw random numbers from a normal (Gaussian) distribution"""
import numpy as np
import matplotlib.pyplot as plt

# initialize random number generator with seed
rng = np.random.default_rng( 42 )

# N normally distributed random numbers
N = 100
nbins = 30
gauss = rng.normal( size=N )

fig, ax = plt.subplots( 2, 1, figsize=([7,10]) )

# plot histogram of random numbers
ax[0].hist( gauss, bins=np.linspace( -3, 3, nbins ) )
ax[0].set_xlabel( "$x$")
ax[0].set_ylabel( "Frequency")

ax[1].hist( gauss, bins=np.linspace( -3, 3, nbins ), density=True, cumulative=True )
ax[1].set_xlabel( "$x$")
ax[1].set_ylabel( "Cumulative Frequency (Normalized)")

plt.savefig( "frequency_gaussian.pdf" )
plt.show()

