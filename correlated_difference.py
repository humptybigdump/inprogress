"""illustrate influence of correlations on uncertainty of difference of two random numbers"""
import numpy as np
import matplotlib.pyplot as plt

# simulate N pairs of random numbers
N = 1000
mu = np.array( [ 5.0, 5.0 ] )
rho12, sigma1, sigma2  = 0.5, 1.0, 1.0
cov = np.array( [[ sigma1**2, rho12*sigma1*sigma2 ],
                 [ rho12*sigma1*sigma2, sigma2**2] ] )

rng = np.random.default_rng( 42 )
x = rng.multivariate_normal( mu, cov, size=N )
diff =  x[:,0] - x[:,1]

# plot
fig, ax = plt.subplots( 2, 1, figsize=([7,12]) )

ax[0].scatter( x[:,0], x[:,1] )
ax[0].set_xlim( 0, 10 )
ax[0].set_ylim( 0, 10 )
ax[0].set_xlabel( "$x_1$" )
ax[0].set_ylabel( "$x_2$" )

bins = np.linspace( -5, 5, 51 )
ax[1].hist( diff, bins=bins, label=r"$\hat\mu=$%5.3f, $\hat\sigma_x=$%5.3f" % ( np.mean( diff ), np.std( diff, ddof=1 ) ) )
ax[1].set_xlabel( "$u = x_1 - x_2$" )
ax[1].set_ylabel( "Frequency" )
ax[1].legend()

plt.savefig( "correlated_difference.pdf" )
plt.show()
