#!/usr/bin/python3 

# script animated_Coin.py
''' example to produce random numbers (0/1) 
    as obtained by throwing a coin
    animated fraction of heads vs. number of throws
    
.. author:: Guenter Quast <g.quast@kit.edu> (a few tweaks by Ulrich Husemann)
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys

nthrow = 499    # how often to throw

#create a figure
fig = plt.figure(figsize=(7.5,7.5))
ax  = fig.add_subplot(1,1,1)
ax.grid(True)
ax.set_xlabel('$N$ (number of trials)', size='x-large')
ax.set_ylabel('$h_{N}$ = $N_h / N$', size='x-large')
x = np.linspace(1,nthrow+1,nthrow)

# plot expectation ...
ax.plot(x,0.5*np.ones(nthrow),'r--',lw=2)
# ... and error band
ax.plot(x,0.5+0.5/np.sqrt(x),'b--',lw=2)
ax.plot(x,0.5-0.5/np.sqrt(x),'b--',lw=2)
txt1 = ax.text(0.1, 0.9, ' ', transform=ax.transAxes,size='xx-large',
  bbox=dict(facecolor='silver', edgecolor='r', boxstyle='circle', pad=0.5))
txt2 = ax.text(0.81, 0.93, ' ', transform=ax.transAxes,size='x-large',
                    backgroundcolor='white')

#
# throw the coin and plot N_head over (number of trials) 
Nh=0
N=0
rng = np.random.default_rng( 42 )

def animate(i):
  global N, Nh, hN, x, rng
  N+=1
  if rng.random() >= 0.5:
    Nh+=1
    t=' O '
  else:
    t='-1-'
  hN = float(Nh)/float(N)
  # plot result 
  graph, = ax.plot(float(N), hN, 'g.')
  txt1.set_text(t)
  txt2.set_text('$N$ = %i' %(N))
  return graph, txt1, txt2
#
# show as animated (=updating) graph
print(('\n*==* script ' + sys.argv[0]+' executing'))
ani=anim.FuncAnimation(fig, animate, nthrow, interval=10, blit=False,
                         init_func=None, fargs=None, repeat=False)
                  
# save animation as movie
Writer = anim.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='UH'), bitrate=1800)
ani.save( "animated_coin.mp4", writer=writer ) 
plt.show()


