"""Example of binary classifications: two fuzzy rings"""

import numpy as np
import matplotlib.pyplot as plt 

rng = np.random.default_rng( 42 )

def random_ring( center=[0,0], radius=1, width=0.2, N=100 ):
    """generate random numbers: radius from normal distribution, uniform polar angle,
    return array of x and y from coordinate transformation, shifted by center"""
    r   = rng.normal( loc=radius, scale=width, size=N )
    phi = rng.uniform( 0, 2*np.pi, size=N )
    return [ center[0]+r*np.cos(phi), center[1]+r*np.sin(phi) ]

# create synthetic data: two intersecting rings
N = 200
ring1 = random_ring( [1,1], 2, 0.2, N )
ring2 = random_ring( [-1,-1], 2, 0.5, N )

fig,ax = plt.subplots()
ax.scatter( ring1[0], ring1[1], color="r", label="Signal" )
ax.scatter( ring2[0], ring2[1], color="b", label="Background" )

# create by-eye discriminant
xl = np.linspace( -3, 3, 300 )
ax.plot( xl, -xl, color="green", linewidth=2, label="Classifier" )
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.legend()

plt.show()