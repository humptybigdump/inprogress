import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


## INPUT

# Spezfiziere Knotenkoordinaten 
XKnoten=np.array([-1.,0.,1.])
YKnoten=np.array([-1.,0.,1.])

# Wähle Ansatzfunktion aus
ID = np.array([0,0]) 

## BERECHNUNG

# Erstelle Raster mit X,Y-Paaren
X = np.arange(min(XKnoten), max(XKnoten), 0.01)
Y = np.arange(min(YKnoten), max(YKnoten), 0.01)
X, Y = np.meshgrid(X, Y)

# Berechne Ansatzfunktion an jedem X,Y-Paar
N=1.
for i in range(len(XKnoten)):
    if i !=int(ID[0]):
        N=N*(X-XKnoten[i])/(XKnoten[int(ID[0])]-XKnoten[i])
for i in range(len(YKnoten)):
    if i !=int(ID[1]):
        N=N*(Y-YKnoten[i])/(YKnoten[int(ID[1])]-YKnoten[i])

# Berechne Ansatzfunktion an jedem Knoten
X2, Y2 = np.meshgrid(XKnoten, YKnoten)
P = np.zeros((len(YKnoten),len(XKnoten)))
P[ID[1],ID[0]]= 1.

##OUTPUT

# Achsenoptionen
fig, ax = plt.subplots(subplot_kw={"projection": "3d", })
ax.set_proj_type('ortho')
ax.set_xlim(min(XKnoten),max(XKnoten))
ax.set_ylim(min(YKnoten),max(YKnoten))
ax.set_zlim(-1.0, 1.0)
ax.xaxis.set_major_locator(LinearLocator(5))
ax.xaxis.set_major_formatter('{x:.01f}')
ax.yaxis.set_major_locator(LinearLocator(5))
ax.yaxis.set_major_formatter('{x:.01f}')
ax.zaxis.set_major_locator(LinearLocator(5))
ax.zaxis.set_major_formatter('{x:.01f}')
ax.set_xlabel('x-axis')
ax.set_ylabel('y-axis')
ax.set_zlabel('N(x,y)')
ax.set_title('Ansatzfunktion für X=%.2f, Y=%.2f'%(XKnoten[ID[0]],YKnoten[ID[1]]))

# Plot
surf = ax.plot_surface(X, Y, N, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.scatter(X2,Y2,P,color='black')
plt.show()