# -*- coding: utf-8 -*-

import numpy as np

# ####### Aufgabe 2.1: 1D-Newton-Verfahren: #####################################

# ## Eingangsdaten:
    
# # Definition der Funktion:
# def f(x):
#     return x * np.exp(- np.sqrt(2) * x) + 0.5 * x + 0.1

# def fdx(x):
#     return np.exp(- np.sqrt(2) * x) - np.sqrt(2) * x * np.exp(- np.sqrt(2) * x) + 0.5

# xStart  =   0                                   # Startwert
# tol     =   10**(-5)                            # Toleranz
# maxIt   =   1000                                # Maximale Iterationszahl

# ## Iteration:
# j   =   0
# xIter   =   [xStart]
# fi      =   f(xIter[-1])
# fdxi    =   fdx(xIter[-1])

# while np.abs(fi) > tol and j <= maxIt:
    
#     j   =   j + 1
#     xIter.append(xIter[-1] - fi / fdxi)
    
#     fi      =   f(xIter[-1])
#     fdxi    =   fdx(xIter[-1])

# if fi <= tol:
#     print('Der Funktionswert an der Stelle x = ' + str(xIter[-1]) + ' beträgt f = ' + str(fi) + '.')
#     print('Für das Newton-Verfahren wurden ' + str(j) + ' Iterationen benötigt.' )
# else:
#     print('Nullstellen-Suche ist fehlgeschlagen!')


####### Aufgabe 2.2: Mehrdimensionales Newton-Verfahren: ######################

## Eingangsdaten:
    
# Definition der Funktion:
def f(x):
    A   =   np.array([[1, 2/3 ,-2], [0, 7, 6/7], [-1/3, 0, 1]])
    a   =   np.array([5, 3, 2])
    f   =   np.linalg.norm(x) * np.einsum('jk, k', A, x) + a
    return f

def fdx(x):
    A   =   np.array([[1, 2/3 ,-2], [0, 7, 6/7], [-1/3, 0, 1]])
    fdx =   1/np.linalg.norm(x) * np.einsum('jk, k, l', A, x, x) + np.linalg.norm(x) * A
    return fdx

xStart  =   np.array([10, 10, 10])                 # Startwert
tol     =   10**(-5)                            # Toleranz
maxIt   =   1000                                # Maximale Iteration
   
## Iteration:
j   =   0
xIter   =   [xStart]
fi      =   f(xIter[-1])
fdxi    =   fdx(xIter[-1]) 

while np.linalg.norm(fi) > tol and j <= maxIt:
    
    j   =   j + 1
    xIter.append(xIter[-1] - np.einsum('ij, j', np.linalg.inv(fdxi), fi))
    
    fi      =   f(xIter[-1])
    fdxi    =   fdx(xIter[-1])

if np.linalg.norm(fi) <= tol:
    print('Der Funktionswert an der Stelle x = ' + str(xIter[-1]) + ' beträgt f = ' + str(fi) + '.')
    print('Für das Newton-Verfahren wurden ' + str(j) + ' Iterationen benötigt.' )
else:
    print('Nullstellen-Suche ist fehlgeschlagen!')

## Plot: 
import matplotlib.pyplot as plt

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

for i in range(j+1):
    fi  =   f(xIter[i])
    ax.scatter(xs = fi[0], ys = fi[1], zs = fi[2], label = str(i))

plt.legend()
plt.show()
