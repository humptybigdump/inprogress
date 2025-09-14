"""PDFs of two-dimensional normal (Gaussian) distributions"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# function to build covariance matrix from variances and correlation coefficient
def build_cov( varx, vary, corr ):
    covxy = corr * np.sqrt( varx*vary )
    return np.array( [ [varx, covxy], [covxy, vary] ] )

# generate a 2D grid to evaluate the PDF 
xmin, xmax = -4, 4
x = np.linspace( xmin, xmax, num=101 )
y = np.linspace( xmin, xmax, num=101 )
X, Y = np.meshgrid( x, y )
pos = np.dstack( (X,Y) )

# start from variances and correlation coefficient, construct covariance matrix
varx1, vary1, corr1 = 2, 2, 0.4
varx2, vary2, corr2 = 2, 2, -0.25

# use scipy.stats class for multivariate normal distributions
Z = []
Z.append( multivariate_normal.pdf( pos, mean=[ 0, 0 ], cov=build_cov( varx1, vary1, corr1 ) ) )
Z.append( multivariate_normal.pdf( pos, mean=[ 0, 0 ], cov=build_cov( varx2, vary2, corr2 ) ) )
fig, ax = plt.subplots( 1, 2, figsize=([12,5]) )

# contour plot with color code
for a, z in zip( ax, Z ):
    a.contourf( X, Y, z, 10, cmap='RdBu' )
    a.set_xlabel( "$x$")
    a.set_ylabel( "$y$" )

plt.savefig( "pdf_gaussian_2d.pdf" )
plt.show()

