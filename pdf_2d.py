""" 
Example plots for two-dimensional PDFs
based on https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/scatter_hist.html#sphx-glr-gallery-lines-bars-and-markers-scatter-hist-py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad

def pdf_2d():
	
	# interval in x and y
	xmin, xmax = 0, 10

	# generate a 2D grid to evaluate the PDF 
	x = np.linspace( xmin, xmax, num=101 )
	y = np.linspace( xmin, xmax, num=101 )
	X, Y = np.meshgrid( x, y )
	Z = function( X, Y )
	
	# sample N random data points from function 
	N, n = 1000000, 1000  
	rng = np.random.default_rng( 42 )
	xyrand = rng.uniform( xmin, xmax, size=(N,2) )
	
	# evaluate function and normalize to unit integral
	func = function( xyrand[:,0], xyrand[:,1] )
	prob = func/np.sum(func)

	# for scatter plot: pick n data points with a probability corresponding to the value of the function
	scatter = rng.choice( xyrand, n, replace=False, p=prob )
	
	# compute marginal distributions by integration
	# condition: independent variable must be first argument -> solved with lambda functions
	func_x = lambda x, y: function( x, y )
	func_y = lambda x, y: function( y, x )

	# integration of marginal distribution using scipy.integrate.quad (adaptive quadrature methods)
	# only use first return variable (value)
	marginal_x = lambda x: quad( func_y, xmin, xmax, args=(x,) )[0]
	marginal_y = lambda y: quad( func_x, xmin, xmax, args=(y,) )[0]
	
	fig = plt.figure( figsize=[12,7] ) 
	ax1 = fig.add_subplot( 221 )
	ax2 = fig.add_subplot( 222 )
	ax3 = fig.add_subplot( 223, projection='3d' )
	ax4 = fig.add_subplot( 224 )
	
	# 2D contour plot using color map
	cont = ax1.contourf( X, Y, Z, cmap='RdBu' )
	cbar = fig.colorbar( cont, ax=ax1 )	
	ax1.set_xlabel( "$x$")
	ax1.set_ylabel( "$y$")
	
	# 3D surface
	cont3d = ax3.plot_surface( X, Y, Z, cmap='RdBu', linewidth=0 )
	cbar3d = fig.colorbar( cont3d, ax=ax3 )

	# scatter plot
	ax2.scatter( scatter[:,0], scatter[:,1], s=1 )
	ax2.set_xlim( xmin, xmax )
	ax2.set_ylim( xmin, xmax )
	
	# 2d histograms
	bins = np.linspace( xmin, xmax, 11 )
	centers = 0.5*( bins[1:] + bins[:-1] )
	XC, YC = np.meshgrid( centers, centers )
	h, xedges, yedges, img = ax4.hist2d( scatter[:,0], scatter[:,1], bins=bins )
	
	# first way to compute profile: by hand using histograms
	"""
	mean value of histogram = weighted mean of bin centers (weight = number of entries)
	standard deviation = weighted standard deviation of bin centers (weight = number of entries)
	both are simple but not very transparent one-liner in NumPy
		mean = np.average( YC, weights=h, axis=0 ) 
	below: implementation "by hand"
	"""
	mean = np.zeros( len(centers) )
	std  = np.zeros( len(centers) )	
	for i, col in enumerate( h ):
		sum = np.sum(col)
		mean[i] = np.sum(col*centers)/sum
		std[i]  = np.sqrt( np.sum( col*centers**2 )/(sum-1) - mean[i]**2 )
	
	# display with error bars
	ax4.errorbar( centers, mean, yerr=std, fmt='wo' )
	ax4.set_xlim( xmin, xmax )
	ax4.set_ylim( xmin, xmax )	
	
	# second way to compute profile: unbinned, directly from data

	# np.digitize: create array of entries' bin indexes 
	idx = np.digitize( scatter, bins )
	
	# array of mean values (using list comprehension)
	unbinned_mean = [ np.mean(scatter[ idx[:,0] == i ], axis=0 )[1] for i in np.arange( 1, 11 ) ]
	# array of sample standard deviations (using list comprehension)
	unbinned_std = [ np.std(scatter[ idx[:,0] == i ], axis=0, ddof=1 )[1] for i in np.arange( 1, 11 ) ]
	
	# display with error bars
	ax2.errorbar( centers, unbinned_mean, yerr=unbinned_std, fmt='bo' )
	ax2.set_xlim( xmin, xmax )
	ax2.set_ylim( xmin, xmax )	

	fig.savefig( 'pdf_2d.pdf' )
	plt.show()
		
	#
	# marginal distributions
	#
	fig = plt.figure( figsize=[12,7] ) 
	ax1 = fig.add_subplot( 221 )
	ax2 = fig.add_subplot( 222 )
	ax3 = fig.add_subplot( 223 )
	ax4 = fig.add_subplot( 224 )

	# 2D contour plot using color map
	cont = ax1.contourf( X, Y, Z, cmap='RdBu' )
	cbar = fig.colorbar( cont, ax=ax1 )	

	ax1.set_ylabel( "$y$")

	xmarg = list( map( marginal_x, x ) )
	ymarg = list( map( marginal_y, y ) )
	
	ax2.plot( x, xmarg )
	ax2.set_xlim( xmin, xmax )
	ax2.set_xlabel( "$x$")
	ax2.set_ylabel( "$f_y(x)$")


	ax3.plot( y, ymarg )
	ax3.set_xlim( xmin, xmax )
	ax3.set_xlabel( "$y$")
	ax3.set_ylabel( "$f_x(y)$")
		
	#
	# conditional probabilities for two example values of x0
	#
	x0 = [ 2, 6 ]
	fx0 = [ function( xi, y ) for xi in x0 ]
	x0marg = list( map ( marginal_x, x0 ) )

	for x, f, m in zip( x0, fx0, x0marg ):
		ax4.plot( y, f/m, label=r"$f(y|x_{0} = %d)$" % x )
	ax4.set_xlabel( "$y$")
	ax4.legend()
	
	fig.savefig( 'pdf_2d_marginal_conditional.pdf' )
	plt.show()
    
    
def function( x, y ):
	"""Example function: product of an exponential and a normal distribution"""
	return np.exp(-0.2*x) * norm.pdf( x+y, loc=7, scale=2 )

if __name__ == '__main__':
    pdf_2d()
