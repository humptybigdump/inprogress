#!/usr/bin/env python

# -------- animaded_convolutionFilter.py -----------------------
# Description: example showing how a convolution filter works
#  for
#      sliding average
#      peak finder
#
# Author:      G. Quast   Nov. 2016
# dependencies: Python 3 numpy, matplotlib.pyplot 
# last modified: U. Husemann, May 2021
#---------------------------------------------------------------

import sys, numpy as np, matplotlib.pyplot as plt
import matplotlib.animation as anim
 
#construct (rectangular) template shapes . . .
# . . . for sliding average
fwidth = 5
kwin=int(fwidth/2)
v_av = np.array([1. for i in range(0, 2*kwin+1)], dtype=np.float32 )

# . . . for peak search
fwidth = 20
kwin=int(fwidth/2)
v_peak = np.array(\
        [-1. for i in range(kwin)] +\
        [ 1. for i in range(2*kwin+1)] +\
        [-1. for i in range(kwin)], 
               dtype=np.float32 )

# . . . for edge search
fwidth = 10
kwin=int(fwidth/2)
v_edge = np.array(\
        [-1. for i in range(2*kwin)] +\
                  [0.] +\
        [1. for i in range(2*kwin)], 
               dtype=np.float32 )

# - - - select template to use in convolution
v=v_av
#v=v_peak
#v=v_edge
k=int(len(v)/2)

# define a signal
xmin, xmax = 0., 30.
N      = 250
xplt   = np.linspace( xmin, xmax, N )
signal = 0.5*np.sin(xplt)+0.25*np.sin(1.3*xplt)+0.25*np.sin(2.5*xplt)

# add some random (Gaussian) noise
rng = np.random.default_rng( 42 )
signal += 0.05 * rng.normal( size=N )

# define and plot initial graphics
fig = plt.figure(figsize=(10., 7.5))
ax = fig.add_subplot(1,1,1)
graph_init = ax.plot(xplt, signal, 'b-')
ax.set_ylabel('Amplitude')
ax.set_xlabel('Position')
ax.set_ylim( -1.1, 1.1 )

scale = (xmax-xmin)/N

# code relevant to parts of figure to animate
graph_signal, = ax.plot( [], [], 'g-', lw=2 )
graph_line,   = ax.plot( [], [], 'r-', lw=3 )
graph_box,    = ax.fill( [], [], color='r', alpha=0.1 )


def animate(n):
  i = n+k 
  signal[i]  = sum( v * signal[i-k:i+k+1] ) / (2*k+1)   
  graph_signal.set_data( xplt[k:i], signal[k:i] )
  graph_line.set_data( np.array( list(range(i-k, i+k+1)))*scale, v )
  graph_box.set_xy( [ [(i-k)*scale,-1], [(i+k)*scale,-1], [(i+k)*scale,1], [(i-k)*scale,1] ] )
  return graph_line, graph_signal, graph_box

print( '\n*==* script ' + sys.argv[0]+' executing' ) 

ani=anim.FuncAnimation( fig, animate, frames=N-2*k, interval=30, repeat=False )

# write an mp4 movie using the ffmpeg encoder (to be installed separately)
Writer = anim.writers[ 'ffmpeg' ]
writer = Writer( fps=30, bitrate=64000 )
ani.save( "smoothing.mp4", writer=writer )
#plt.savefig( "peak_filter.pdf")

plt.show()
