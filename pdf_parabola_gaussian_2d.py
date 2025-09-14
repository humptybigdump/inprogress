"""PDF of parabola times Gaussian distribution"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def function( x, y ):
	"""Gaussian along a parabola y=p(x): use p(x)-y as argument of Gaussian"""
	return norm.pdf( 2. - 0.2*x**2 - y )

# create 2D grid to evaluate 2D function
xmin, xmax = -5, 5
x = np.linspace( xmin, xmax, num=101 )
y = np.linspace( xmin, xmax, num=101 )
X, Y = np.meshgrid( x, y )

Z = function( X, Y )

fig, ax = plt.subplots(1,1,figsize=([10,7]) )

# contour plot with color bar for values
cont = ax.contourf( X, Y, Z, 10, cmap='RdBu' )	
cbar = fig.colorbar( cont, ax=ax )	
ax.set_xlabel( "$x$")
ax.set_ylabel( "$y$" )

plt.savefig( "pdf_parabola_gaussian_2d.pdf" )
plt.show()

