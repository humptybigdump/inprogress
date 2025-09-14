"""PDF of uniform distribution: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import uniform

# range of x values
x = np.linspace( -0.1, 10.1, 200 )

fig, ax = plt.subplots()

# uniform distributions in for different intervals
intervals = [ [0,1], [3,6], [2,9], [6.5,8] ]
for a, b in intervals:
	pdf = uniform.pdf( x, loc=a, scale=b-a )
	line, = ax.plot( x, pdf )

	# compute maximum of PDF, expected value and standard deviation
	max = 1/(b-a)
	E  = 0.5*(a+b)
	sd = (b-a)/np.sqrt(12)

	# plot vertical line at expected value
	ax.vlines( E, 0, max )

	# plot transparent rectangle covering +/- one standard deviation around expected value
	rect = mpatches.Rectangle( ( E-sd, 0 ), width=2*sd, height=max, color=line.get_color(), alpha=0.3 )
	ax.add_patch( rect )

ax.set_xlabel( "$x$")
ax.set_ylabel( "Probability Density Functions" )

plt.savefig( "pdf_uniform.pdf" )
plt.show()

