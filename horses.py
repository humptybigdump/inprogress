"""Prussian army members killed by horse kick (L. von Bortkewitsch, 1898)"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

n = np.arange( 5 )
# data based on 10 army corps with 20 troops ("escadrons") 
# with about 150 hourses each over 20 years
k = np.array( [109, 65, 22, 3, 1] )
N = np.sum( k )

# Poisson expectation for nu = 0.61
nu = 0.61
pois = N*poisson.pmf( n, nu )

fig, ax = plt.subplots()
ax.bar( n-0.20, pois, width=0.4, label=r"Poisson, $\nu=%4.2f$" % nu )
ax.bar( n+0.20, k, width=0.4, label="Data" )
ax.set_xlabel( "Number of Army Members Killed per Year" )
ax.set_ylabel( "Number" )
ax.legend()

plt.savefig( "horses.pdf" )
plt.show()