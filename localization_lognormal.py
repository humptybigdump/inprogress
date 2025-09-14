"""PDF of the log-normal distribution with different localization parameters"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

x = np.linspace( 0, 5, 200 )

scale = 1.0
pdf = lognorm.pdf( x, s=scale )

localization = [ np.exp(-1), lognorm.median( s=scale ), lognorm.mean( s=scale ) ]
locname = [ "Mode", "Median", "Mean" ]
colors = [ "red", "green", "blue" ]

ymin, ymax = 0, 1.1*np.amax(pdf)

plt.plot( x, pdf )
plt.ylim( ymin, ymax )
plt.vlines( localization, ymin, ymax, colors=colors, linestyles="dashed" )
for l,n,c in zip(localization, locname, colors):
    plt.text( l+0.05, lognorm.pdf( l, s=scale )+0.01, n, color=c )

plt.xlabel( "$x$")
plt.ylabel( "Probability Density Function" )

plt.savefig( "localization_lognormal.pdf" )
plt.show()