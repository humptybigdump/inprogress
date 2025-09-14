"""illustrate different ways of representing distributions and uncertainties"""
import numpy as np
import matplotlib.pyplot as plt

def errorbars( data, ax ):

    # lines at the random data
    ax.vlines(data, 0, 1, linestyles='-', lw=2)

    # classic uncertainty bar symbolizing uncertainty of mean
    meanx = np.mean( data )
    meany = 2.
    stdx  = np.std( data, ddof=1 )/np.sqrt( len(data) )
    ax.errorbar( meanx, meany, xerr=stdx, fmt='-go' )

    # non-standard uncertainty bar symbolizing spread of distribution itself
    meanx = np.mean( data )
    meany = 3.
    stdx  = np.std( data, ddof=1 )
    ax.errorbar( meanx, meany, xerr=stdx, fmt='-ro' )

    # box-whisker plot
    boxy = 4.
    ax.boxplot( data, positions=[boxy], vert=False , notch=False )

    ax.set_ylim( 0, 5 )
    ax.set_yticks ( [] )
    ax.set_xlabel( "$x$") 

    return 

rng = np.random.default_rng(42)
n = 100

fig,ax = plt.subplots( 2, 1, figsize=(7,10) )

errorbars( rng.normal( size=n ), ax[0] )
errorbars( rng.exponential( size=n ), ax[1] )

plt.savefig( "data_errorbars.pdf" )
plt.show()

