"""Python code demonstrating statistical uncertaintly of the mean value"""
import numpy as np
import matplotlib.pyplot as plt

# simulation n series of N measurements each
n, N = 1000, 9

# initialize random number generator and draw from normal distribution
rng = np.random.default_rng( 42 )
x = rng.normal( size=(n,N) )

# flatten array of random numbers to look at full distribution
x_all =  x.flatten()

# distribution of mean values of n distributions of N measurements (projection to axis 1)
x_grp = np.mean( x, axis=1 )

# plot the results
fig, ax = plt.subplots(1,2,figsize=([15,5]) )
bins = np.linspace( -5, 5, 51 )
ax[0].hist( x_all, bins=bins, label=r"$\hat\mu=$%5.3f, $\hat\sigma_x=$%5.3f" % ( np.mean( x_all ), np.std( x_all, ddof=1 ) ) )
ax[0].set_xlabel( "$x$")
ax[0].set_ylabel( "Frequency")
ax[0].legend()

ax[1].hist( x_grp, bins=bins, label=r"$\hat\mu=$%5.3f, $\sigma_{\hat\mu}=$%5.3f" % ( np.mean( x_grp ), np.std( x_grp, ddof=1 ) ) )
ax[1].set_xlabel( "$x$")
ax[1].set_ylabel( "Frequency")
ax[1].legend()

plt.savefig( "uncertainty_mean_value.pdf" )
plt.show()

