"""least squares: graphical solution for variance"""
import numpy as np
import matplotlib.pyplot as plt

# true model parameters
atrue = 3
sig   = 1

# data points
N = 5
xi = np.linspace( 1, N, N )

# scan of a values
amin, amax, steps = 2, 4, 200
a = np.linspace( amin, amax, steps )

rng = np.random.default_rng( 42 )
yi = rng.normal( loc=atrue, scale=sig, size=N )

# plot
fig,ax = plt.subplots()

# compared to the code example above, this is an alternative way to compute S using list comprehension
S_plot = np.array( [ np.sum( ( ( yi - a_plot ) / sig )**2 ) for a_plot in a ] )

# this is a way to compute the minimum of the curve and the interval
S_min = S_plot.min()    # minimal value of S
i_min = S_plot.argmin() # index of minimal value
i_sigma, = np.where( S_plot < S_min+1 ) # range of indices where S is below S_min+1, first and last index are +/- 1 sigma

ax.plot( a, S_plot )
ax.set_xlabel( r"$a$")
ax.set_ylabel( r"$S(a)$")
ax.set_xlim( amin, amax )
ax.set_ylim( 5, 12 )

ax.vlines( (a[i_min], a[i_sigma[0]], a[i_sigma[-1]]), 5, 10, linestyles="dashdot" )
ax.hlines( (S_min,S_min+1), amin, amax, linestyles="dashed" )

ax.text( 3.75, S_min+0.1, r"$\Delta \chi^2=0$" )
ax.text( 3.75, S_min+1.1, r"$\Delta \chi^2=1$" )
ax.text( a[i_min], 10.2, r"$\hat{a}$", ha="center")
ax.text( a[i_sigma[0]], 10.2, r"$\hat{a}-\sigma_{\hat{a}}$", ha="center")
ax.text( a[i_sigma[-1]], 10.2, r"$\hat{a}+\sigma_{\hat{a}}$", ha="center")

plt.savefig("ls_variance.pdf")
plt.show()