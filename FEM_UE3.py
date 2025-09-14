import matplotlib.pyplot as plt
import numpy as np


## INPUT

# Spezifiziere Knotenanzahl
m = [2,3,4,5]

# Spezfiziere Quadratur
# Mögliche Quadraturen: NewtonCotesOffen, NewtonCotesGeschlossen, Gauss
ID = ['NewtonCotesOffen', 'NewtonCotesGeschlossen', 'Gauss']

# Spezifiziere Intervall
xBounds = np.array([0,5])

# Spezifiziere Funktion
def Funktion(x):
    return x**4 + 2*x

## Integration
def integriereFunktion(m,ID):
    # Stützstellen
    def ReferenzStützstellen(m,ID):
        xii = np.zeros(m)
        wi = np.zeros(m)
        if ID == 'NewtonCotesOffen':
            import sympy as sym
            xi = sym.Symbol('xi')
            h = 2 / m
            for i in range(m):
                xii[i] = -1 + h / 2 + i * h
            for i in range(m):
                p = 1
                for j in range(m):
                    if j != i:
                        p *= (xi - xii[j]) / (xii[i] - xii[j])
                wi[i] = sym.integrate(p, (xi,-1 ,1 ))
            
        elif ID == 'NewtonCotesGeschlossen':
            import sympy as sym
            xi = sym.Symbol('xi')
            for i in range(m):
                xii[i] = -1 + i * 2/(m-1)
            for i in range(m):
                p = 1
                for j in range(m):
                    if j != i:
                        p *= (xi - xii[j]) / (xii[i] - xii[j])
                wi[i] = sym.integrate(p, (xi,-1 ,1 ))
                
        elif ID == 'Gauss':
            xii, wi = np.polynomial.legendre.leggauss(m)
            
        return xii, wi
    
    xii, wi = ReferenzStützstellen(m,ID)
    
    # Transformation auf gegebenes Intervall: 
    xi = (xBounds[1] - xBounds[0]) / 2 * xii + (xBounds[1] + xBounds[0]) / 2
    
    # Integration der Funktion:
    Ergebnis = 0
    for i in range(m):
        Ergebnis += wi[i] * Funktion(xi[i])
    Ergebnis *= (xBounds[1] - xBounds[0]) / 2
    
    return Ergebnis

############### BERECHNUNG MIT DEFINIERTEM INPUT ############################

exaktesErgebnis = 650
numerischesErgebnis = np.zeros((len(m), len(ID)))

for i in range(len(m)):
    for j in range(len(ID)):
        numerischesErgebnis[i,j] = integriereFunktion(m[i], ID[j])

############### Graphischer Output ############################
color = ['green', 'red', 'blue']

for i in range(len(ID)):
    plt.scatter(m, numerischesErgebnis[:,i],c=color[i],label=ID[i])
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Numerische Integration")
plt.xticks(m)
plt.legend()
plt.show()

for i in range(len(ID)):
    plt.scatter(m[1:], numerischesErgebnis[1:,i],c=color[i],label=ID[i])
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Numerische Integration")
plt.xticks(m[1:])
plt.legend()
plt.show()

