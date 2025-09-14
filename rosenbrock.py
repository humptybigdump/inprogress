#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""Rosenbrock function: standard example of numerical optimization"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x = np.linspace( -1.5, 1.5, 300 )
y = np.linspace( -1, 2, 300 )
X, Y = np.meshgrid( x, y )

rosen = lambda x, y: ( 1 - x )**2 + 100*( y - x**2 )**2
Z = rosen( X, Y )
levels = np.logspace( -2, 3, 16 )

fig, ax = plt.subplots()
CS = ax.contourf( X, Y, Z, levels, cmap=matplotlib.cm.gray, norm=matplotlib.colors.LogNorm() )
fig.colorbar( CS, ax=ax )
ax.set_xlabel( r'$x$' )
ax.set_ylabel( r'$y$' )

fig.savefig( 'rosenbrock.pdf' )
plt.show()
