import matplotlib.pyplot as plt
import numpy as np

# Knotenposition und Knotenwerte
Knoten = np.array([-1,0,1,2])
Verschiebung = np.array([1,0,1,4])

X = np.arange(Knoten[0], Knoten[-1], 0.01)

# Ansatzfunktionen N(x)
N = np.ones([len(Knoten),len(X)])
B = np.ones([len(Knoten),len(X)])

N[0,:] = (X-Knoten[1])/(Knoten[0]-Knoten[1]) * (X-Knoten[2])/(Knoten[0]-Knoten[2]) * (X-Knoten[3])/(Knoten[0]-Knoten[3])
N[1,:] = (X-Knoten[0])/(Knoten[1]-Knoten[0]) * (X-Knoten[2])/(Knoten[1]-Knoten[2]) * (X-Knoten[3])/(Knoten[1]-Knoten[3])
N[2,:] = (X-Knoten[0])/(Knoten[2]-Knoten[0]) * (X-Knoten[1])/(Knoten[2]-Knoten[1]) * (X-Knoten[3])/(Knoten[2]-Knoten[3])
N[3,:] = (X-Knoten[0])/(Knoten[3]-Knoten[0]) * (X-Knoten[1])/(Knoten[3]-Knoten[1]) * (X-Knoten[2])/(Knoten[3]-Knoten[2])

B[0,:] = 1/(Knoten[0]-Knoten[1]) * (X-Knoten[2])/(Knoten[0]-Knoten[2]) * (X-Knoten[3])/(Knoten[0]-Knoten[3]) + (X-Knoten[1])/(Knoten[0]-Knoten[1]) * 1/(Knoten[0]-Knoten[2]) * (X-Knoten[3])/(Knoten[0]-Knoten[3]) + (X-Knoten[1])/(Knoten[0]-Knoten[1]) * (X-Knoten[2])/(Knoten[0]-Knoten[2]) * 1/(Knoten[0]-Knoten[3])
B[1,:] = 1/(Knoten[1]-Knoten[0]) * (X-Knoten[2])/(Knoten[1]-Knoten[2]) * (X-Knoten[3])/(Knoten[1]-Knoten[3]) + (X-Knoten[0])/(Knoten[1]-Knoten[0]) * 1/(Knoten[1]-Knoten[2]) * (X-Knoten[3])/(Knoten[1]-Knoten[3]) + (X-Knoten[0])/(Knoten[1]-Knoten[0]) * (X-Knoten[2])/(Knoten[1]-Knoten[2]) * 1/(Knoten[1]-Knoten[3])
B[2,:] = 1/(Knoten[2]-Knoten[0]) * (X-Knoten[1])/(Knoten[2]-Knoten[1]) * (X-Knoten[3])/(Knoten[2]-Knoten[3]) + (X-Knoten[0])/(Knoten[2]-Knoten[0]) * 1/(Knoten[2]-Knoten[1]) * (X-Knoten[3])/(Knoten[2]-Knoten[3]) + (X-Knoten[0])/(Knoten[2]-Knoten[0]) * (X-Knoten[1])/(Knoten[2]-Knoten[1]) * 1/(Knoten[2]-Knoten[3])
B[3,:] = 1/(Knoten[3]-Knoten[0]) * (X-Knoten[1])/(Knoten[3]-Knoten[1]) * (X-Knoten[2])/(Knoten[3]-Knoten[2]) + (X-Knoten[0])/(Knoten[3]-Knoten[0]) * 1/(Knoten[3]-Knoten[1]) * (X-Knoten[2])/(Knoten[3]-Knoten[2]) + (X-Knoten[0])/(Knoten[3]-Knoten[0]) * (X-Knoten[1])/(Knoten[3]-Knoten[1]) * 1/(Knoten[3]-Knoten[2])

U = np.zeros(len(X))
E = np.zeros(len(X))

for i in range(len(Knoten)):
    U += N[i,:]*Verschiebung[i]
    E += B[i,:]*Verschiebung[i]

plt.plot(X,U)
plt.plot(X,E)
plt.scatter(Knoten,Verschiebung,color='black')
plt.xlabel("x-Koordinate")
plt.ylabel("Feld")
plt.legend(['Verschiebung','Dehnung'])
plt.show()