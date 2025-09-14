"""Compare synthetic data from a linear model and fit to a linear and quadratic model"""
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
from scipy.stats import chi2

# range of values
n, xmin, xmax = 10, 1., 10.
xdata = np.linspace( xmin, xmax, n )

def lin_model( x, a0=1., a1=1. ):
	'''linear model (straight line)'''
	return a0 + a1*x
	
def quad_model( x, a0=1., a1=1., a2=1. ):
	'''quadratic model (parabola)'''
	return a0 + ( a1 + a2*x ) * x
	
def fit_model( func, name, ey, ax, abs_sigma=True ):
    """fit to synthetic data using scipy.optimize.curve_fit"""
	
    # perform the fit
	# Note: 
    popt, pcov = curve_fit( func, xdata, ydata, sigma=ey, absolute_sigma=abs_sigma )

    # compute sum of squared residuals "manually"
    S = np.sum( ( ( ydata - func( xdata, *popt ) ) / ey  )**2 )
    ndof = n - len( popt ) # number of data points minus number of parameters
    prob = 1. - chi2.cdf( S, ndof )
    print( "Results using scipy.optimize.curve_fit (%s model)" % name )
    print( "  Parameters:                  ", popt )
    print( "  Uncertainties:               ", np.sqrt( np.diag(pcov) ) )
    print( "  Covariance matrix:\n", pcov )
    print( "  chi2, ndof, chi2/ndof, prob: ", S, ndof, S/ndof, prob )

    # plot
    ax.set_ylim( 0, 5 )
    ax.errorbar( xdata, ydata, yerr=ey, fmt='bo')
    ax.plot( xrange, func( xrange, *popt), 'r' ) 
    ax.text( 1, 4.5, "%s model:" % name )
    ax.text( 1, 4.25, r"$\chi^2/n_{\mathsf{dof}} = %4.2f/%d$" % (S, ndof))
    ax.text( 1, 4.0, r"$P_{\chi^2} = %4.2e$" % prob )
    if( func == lin_model ):
        ax.text( 1, 3.75, r"$\hat{a}_0 = %4.2f \pm %4.2f$" % ( popt[0], np.sqrt( pcov[0][0] ) ) )
        ax.text( 1, 3.5, r"$\hat{a}_1 = %4.2f \pm %4.2f$" % ( popt[1], np.sqrt( pcov[1][1] ) ) )

    return

# true parameter values
lin_model_pars  = [ 1.0, 0.3 ]

# relative uncertaintly of y values (assuming x values do not have uncertainties)
ey_rel = 0.1

# use hard-coded xy values according to this model directly
xrange = np.linspace( 0.5, 10.5, 200 )
xdata = np.array( [ 1.,  2.,  3.,  4. , 5.,  6. , 7.,  8.,  9., 10.] )
ydata = np.array( [ 1.23912799, 1.59626873, 1.69944363, 1.95397332, 2.26423559, 3.20817472, 3.12755677, 3.09552808, 3.39170581, 4.31564169 ] )


# fit and plot linear and quadratic model to four different uncertainty models
fig,ax = plt.subplots( 2, 4, figsize=(15,10))

# uncertainty model 1: 10% relative to true y value
ey1 = 0.1 * lin_model( xdata, *lin_model_pars ) 
fit_model( lin_model, "linear", ey1, ax[0][0] )
fit_model( quad_model, "quadratic", ey1, ax[1][0] )

# uncertainty model 2: all uncertainties divided by two
ey2 = 0.5*ey1
fit_model( lin_model, "linear", ey2, ax[0][1] )
fit_model( quad_model, "quadratic", ey2, ax[1][1] )

# uncertainty model 3: the Excel way – all uncertainties = 1
ey3 = np.ones( n ) 
fit_model( lin_model, "linear", ey3, ax[0][2] )
fit_model( quad_model, "quadratic", ey3, ax[1][2] )

# uncertainty model 4: curve_fit default - scaling of covariance matrix for chi2/dof=1
ey4 = ey1
fit_model( lin_model, "linear", ey4, ax[0][3], False )
fit_model( quad_model, "quadratic", ey4, ax[1][3], False )

plt.savefig("GoF.pdf")
plt.show()