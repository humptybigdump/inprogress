#!/usr/bin/env python
# script animate_autoCorrelatoin
''' calculation the autocorrelation function
    with animated illustration
.. author:: Guenter Quast <g.quast@kit.edu>
'''

# dependencies:  Python v3.12, numpy, matplotlib
# last modified: U. Husemann, March 2024
#--------------------------------------------------------------

import numpy as np, matplotlib.pyplot as plt, sys
import matplotlib.animation as anim

##### ---- main program starts here -----
if __name__ == "__main__":

	print(('\n*==* script ' + sys.argv[0]+' executing'))

	# read data
	data = np.genfromtxt('phyphox_voice.csv', delimiter=",", skip_header=1 )
	print(" --> number of columns", data.shape[0])
	print(" --> number of rows", data.shape[1])

	# use only the first 250 entries
	#t = data[:,0]    
	#y = data[:,1]
	t = data[:250,0]
	y = data[:250,1]
 
	N = len(y)  
	
	# generate and plot static part of figure
	fig = plt.figure( figsize=(10.,7.5) )
	ax1 = fig.add_subplot( 2,1,1 )
	ax2 = fig.add_subplot( 2,1,2 )
	ax1.grid( True )
	ax2.grid( True )
	
	ax1.set_title( 'Autocorrelation of a periodic signal', size='xx-large' )
	ax1.set_xlabel( 'Time (ms)' )
	ax2.set_xlabel( 'Time Difference (ms)' )
	ax1.set_ylabel( 'Amplitude')
	ax2.set_ylabel( r'Autocorrelation $\rho$' )
  	
	timetxt = ax1.text(0.3, 0.9, ' ', transform=ax1.transAxes,size='large',               backgroundcolor='white')
                    	
	# plot dummy versions of all objects for later animation
	graph1,  = ax1.plot( t, y, '-', color='black' )
	graph1a, = ax1.plot( [], [], '-', color='blue', lw=2 )
	graph1b, = ax1.plot( [], [], '-', color='blue', lw=2 )
	graph1c  = ax1.axvline( color='darkred')
	graph2, = ax2.plot( t, np.zeros( len(t) ), '--', color='black', lw=1 )
  	
	ax2.set_ylim(-1.,1.)
	
	# variables for dynamic part   
	nrep = N-1 # number of repetitions	
	rho    = np.zeros( N )   # vector for autocorrelations (calulated in animate)
	rho[0] = np.inner( y, y )

	def animate(n):
    	# animation loop
		global rho
		
		i = n+1
		# calculate autocorrelation at i as inner product
		rho[i] = np.inner(y[i:], y[:-i])/rho[0] 
		
		# update animation objects
		graph1a.set_data( t[i:], y[:-i] )
		graph1b.set_data( t[i:], y[i:] )
		graph1c.set_xdata( [t[i]] ) # must be a sequence type, even for a single value
		graph2, = ax2.plot(t[:i], rho[:i], '-', color='darkred', lw=2)
		timestep='i=%i' %(i)
		timetxt.set_text(timestep)
		return graph1a, graph1b, graph1c, graph2, timetxt

	# excute animation (calls animate() nrep times every 30 ms)  
	ani=anim.FuncAnimation( fig, animate, frames=nrep, interval=50, repeat=False )
       
	# write an mp4 movie using the ffmpeg encoder (to be installed separately)
	#Writer = anim.writers[ 'ffmpeg' ]
	#writer = Writer( fps=30, bitrate=64000 )
	#ani.save( "autocorr.mp4", writer=writer )
	plt.savefig( "autocorr.pdf")
                         
	plt.show()
