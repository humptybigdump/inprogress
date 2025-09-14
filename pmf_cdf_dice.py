""" 
Probability mass function and cumulative distribution function 
for discrete measurement results: example of dice
"""
import numpy as np
import matplotlib.pyplot as plt

# number of faces on dice
n = 6

# for probability: array with exactly one entry for each number
throws = np.arange( 1, n+1 )

# probability mass function
pmf = 1/n * np.ones( n )

# commulative distribution function
cdf = np.cumsum( pmf )

fig, ax = plt.subplots( 2, 1, figsize=([7,10]) )

# alternative representation using histograms
#ax[0].hist( throws, bins=np.linspace( 0.5, 6.5, 7 ), density=True )

# representation with bar charts
ax[0].bar( throws, pmf )
ax[0].set_xlabel( "Number")
ax[0].set_ylabel( "Probability Mass Function")

# alternative representation using histograms
#ax[1].hist( throws, bins=np.linspace( 0.5, 6.5, 7 ), density=True, cumulative=True )

# representation with bar charts
ax[1].bar( throws, cdf )
ax[1].set_xlabel( "Number")
ax[1].set_ylabel( "Cumulative Distribution Function")

plt.savefig( "pmf_cdf_dice.pdf" )
plt.show()

