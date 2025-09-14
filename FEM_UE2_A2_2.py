import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

# Knotenanzahl
Knoten=np.array([2,3,4,5,6])
Temperatur=np.array([3,1,0,-1,2])

X = np.arange(Knoten[0], Knoten[-1], 0.01)

# Ansatzfunktionen N(x)
N=np.ones([len(Knoten),len(X)])
N[0,:] = (X-Knoten[1])/(Knoten[0]-Knoten[1]) * (X-Knoten[2])/(Knoten[0]-Knoten[2]) * (X-Knoten[3])/(Knoten[0]-Knoten[3]) * (X-Knoten[4])/(Knoten[0]-Knoten[4])
N[1,:] = (X-Knoten[0])/(Knoten[1]-Knoten[0]) * (X-Knoten[2])/(Knoten[1]-Knoten[2]) * (X-Knoten[3])/(Knoten[1]-Knoten[3]) * (X-Knoten[4])/(Knoten[1]-Knoten[4])
N[2,:] = (X-Knoten[0])/(Knoten[2]-Knoten[0]) * (X-Knoten[1])/(Knoten[2]-Knoten[1]) * (X-Knoten[3])/(Knoten[2]-Knoten[3]) * (X-Knoten[4])/(Knoten[2]-Knoten[4])
N[3,:] = (X-Knoten[0])/(Knoten[3]-Knoten[0]) * (X-Knoten[1])/(Knoten[3]-Knoten[1]) * (X-Knoten[2])/(Knoten[3]-Knoten[2]) * (X-Knoten[4])/(Knoten[3]-Knoten[4])
N[4,:] = (X-Knoten[0])/(Knoten[4]-Knoten[0]) * (X-Knoten[1])/(Knoten[4]-Knoten[1]) * (X-Knoten[2])/(Knoten[4]-Knoten[2]) * (X-Knoten[3])/(Knoten[4]-Knoten[3])

T=np.zeros(len(X))

for i in range(len(Knoten)):
    T += N[i,:]*Temperatur[i]

plt.plot(X,T)
plt.scatter(Knoten,Temperatur,color='black')
plt.xlabel("x-Koordinate")
plt.ylabel("Temperatur")
plt.show()