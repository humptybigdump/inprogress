"""animated_leastSquares: illustration of least squares method"""
# U. Husemann, June 2021

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

# model
atrue = 3
sig   = 1

# data points
n = 10
xi = np.linspace( 1, n, n )

# scan possible values of parameter a
amin, amax, steps = 0., 6., 300
a = np.linspace( amin, amax, steps )

rng = np.random.default_rng( 42 )
yi = rng.normal( loc=atrue, scale=sig, size=n )

fig,ax = plt.subplots( 2, 1, figsize=(7,10) )
graph_data  = ax[0].errorbar( xi, yi, yerr=sig, fmt='ro')
graph_line, = ax[0].plot( [], [], 'b-', lw=2 )
graph_S,    = ax[1].plot( [], [], 'b-', lw=2 )
ax[0].set_xlabel( r"$x$")
ax[0].set_ylabel( r"$y$")
ax[0].set_ylim( amin, amax )
ax[1].set_xlabel( r"$a$")
ax[1].set_ylabel( r"$S$")
ax[1].set_xlim( amin, amax )
ax[1].set_ylim( 0, 100 )

def S( a, y, sig=1. ):
	return np.sum( ( ( y - a ) / sig )**2 )

def animate( step ):
	a_anim = a[:step+1]
	S_anim = [ S( a, yi, sig ) for a in a_anim ]
	graph_line.set_data( [0.5,10.5], [a_anim[-1],a_anim[-1]] )
	graph_S.set_data( a_anim, S_anim )
	return graph_line, graph_S

ani = anim.FuncAnimation( fig, animate, frames=steps, interval=30, repeat=False )

# write an mp4 movie using the ffmpeg encoder (to be installed separately)
Writer = anim.writers[ 'ffmpeg' ]
writer = Writer( fps=30, bitrate=64000 )
ani.save( "least_squares.mp4", writer=writer )
#plt.show()