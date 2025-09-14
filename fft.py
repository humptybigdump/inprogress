#!/usr/bin/env python
#-*- coding: utf-8 -*-

""" FFT: fast Fourier transformation """

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# read audio signal
data = np.genfromtxt('phyphox_voice.csv', delimiter=",", skip_header=1 )
t = data[:,0]    
x = data[:,1]
N = len(x) 
sampling = 48000 # match Phyphox's default sampling frequency: 48 kHz

# FFT routine from NumPy
fft  = np.fft.rfft( x )
freq = np.linspace( 0, 0.5*sampling, int( 0.5*N ) + 1 ) 

# plotting the results
fig,ax = plt.subplots( 2, 1, figsize=(12,8))
ax[0].plot( t, x )
ax[0].set_xlabel( r'$t$ (ms)' )
ax[0].set_ylabel( r'Signal height in time domain (arbitrary units)' )

ax[1].plot( freq, np.abs( fft ) )
ax[1].set_xlabel( r'$\nu$ (Hz)' )
ax[1].set_ylabel( r'Signal height in frequency domain (arbitrary units)' )
ax[1].set_xlim( 0, 0.1*sampling )

plt.savefig( 'fft.pdf', bbox_inches='tight' ) 
plt.show()
