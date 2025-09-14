"""Plot PDF of Cauchy distribution with different parameter choices"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import cauchy

# create Cauchy PDFs for array of parameters x0 and Gamma
param = np.array( [ [ 0., 1.] , [-1., 0.5], [ 0., 2. ] ] )
x = np.linspace( -5, 5, 200 )
pdf  = [ cauchy.pdf( x, loc=l, scale=s ) for l, s in param ]

ymin, ymax = 0, 1.1*np.amax(pdf)

for p, par in zip( pdf, param ):
	# plot Cauchy distributions and add entry in legend
	plot = plt.plot( x, p, label=r"$x_{0} = %3.1f,\,\Gamma = %3.1f$" % (par[0],par[1])  )

	# get minimum/maximum x values for line
	sigmin, sigmax = par[0]-par[1], par[0]+par[1]

	# get y value from evaluating PDF at sigmax
	ysig = cauchy.pdf( sigmax, loc=par[0], scale=par[1] )

	# draw dashed line from x=sigmin to x=sigmax at y=ysig
	plt.hlines( ysig, sigmin, sigmax, color=plot[-1].get_color(), linestyle="dashed" )
	
plt.ylim( ymin, ymax )
plt.xlabel( "$x$")
plt.ylabel( "Probability Density Distribution" )
plt.legend()

plt.savefig( "variance_cauchy.pdf" )
plt.show()

