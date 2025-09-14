#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" Autocorrelation """
import numpy as np
import matplotlib

import matplotlib.pyplot as plt
from scipy import signal

# generate signal
nt = 500
tmin, tmax = 0, 50
times = np.linspace( tmin, tmax, nt )
signal = np.sin( times + 0.5 ) 

# add square wave noise
rng = np.random.default_rng( 42 )
noise = rng.uniform( -0.5, 0.5, nt )
signal += noise

# autocorrelation using np.correlate: mode='full' yields mirrored autocorrelation function in addition
autocorr = np.correlate( signal, signal, mode='full' )
autocorr /= autocorr[nt-1] # normalize

# autocorrelation using scalar product
gsignal, gnoise = np.zeros( nt ), np.zeros( nt )
gsignal[0] = np.inner( signal, signal )
gnoise[0] = np.inner( noise, noise )
for i in np.arange( 1, nt ):
    gsignal[i] = np.inner( signal[:-i], signal[i:] )
    gnoise[i] = np.inner( noise[:-i], noise[i:] )
acsignal = gsignal/gsignal[0]
acnoise  = gnoise/gnoise[0]


# plot results
fig,ax = plt.subplots( 2, 2, figsize=(8,8))
ax[0][0].plot( times, noise )
ax[0][0].set_xlabel( r'$t$ (arbitrary units)' )
ax[0][0].set_ylabel( r'Amplitude (arbitrary units)' )

ax[0][1].plot( times, acnoise )
ax[0][1].set_xlabel( r'$\tau$  (arbitrary units)' )
ax[0][1].set_ylabel( r'Amplitude (arbitrary units)' )

ax[1][0].plot( times, signal )
ax[1][0].set_xlabel( r'$t$  (arbitrary units)' )
ax[1][0].set_ylabel( r'Amplitude (arbitrary units)' )

ax[1][1].plot( times, acsignal )
ax[1][1].set_xlabel( r'$\tau$ ( (arbitrary units)' )
ax[1][1].set_ylabel( r'Amplitude (arbitrary units)' )

plt.savefig( 'autocorrelation.pdf', bbox_inches='tight' ) 
plt.show()
