# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:45:55 2022

@author: Celine Lauff
"""
import numpy as np
from sympy import Matrix, zeros, shape, sqrt
import sympy as sym

####### Eingangsdaten #########################################################

## Materialdaten:
E   =   3 * 10 ** 7                                         # Elastizitätsmodul                       
nu  =   0.3                                                 # Querdehnzahl

## Lasten (nur Randlasten!):
# Streckenlasten bzgl. des Referenzelementes:
# 1. Zeile: Randlast bei eta = -1, 2. Zeile: Randlast bei xi = 1, 
# 3. Zeile: Randlast bei eta = 1, 4. Zeile: Randlast bei xi = -1
tStrecken   =   []
tStrecken.append(Matrix([[0, 0],
                 [0, 0],
                 [0, 0],
                 [0, -20]]))   
tStrecken.append(Matrix([[0, 0],
                 [0, 0],
                 [0, 0],
                 [0, -20]]))   
# Knotenlasten der 8 Freiheitsgrade des Elementes:
tKnoten   =   []
tKnoten.append(Matrix([[0, 0, 0, 0, 0, 0, 0, 0]]).T)
tKnoten.append(Matrix([[0, 0, 0, 0, 0, 0, 0, 0]]).T)
    
## Definition der Elemente und Knotenfreiheitsgrade:
e   =   2                                                   # Elementanzahl                     
# Elementknoten-Koordinaten in x
x   =   []                                
x.append(Matrix([[0, 0, 1, 1]]).T)
x.append(Matrix([[1, 1, 2, 2]]).T)
# Elementknoten-Koordinaten in y
y   =   []                                
y.append(Matrix([[1, 0, 0.25, 1]]).T)
y.append(Matrix([[1, 0.25, 0.5, 1]]).T)
# Elementzuordnungsmatrix
L   =   []                                
L.append(Matrix([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]))
L.append(Matrix([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])) 
# Anzahl der Knotenverschiebungen (gehalten und frei):
numdf   =   shape(L[0])[1]
# LF-Matrix zur Partitionierung
LF   =   Matrix([[0, 0, 0, 0, 0, 0, 0, 0],          
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1]])                                

assert (len(x) == e and len(y) == e and len(L) == e), 'Falsche Definition der Elemente'
                                                               
## Vorgaben für die numerische Integration:
n   =   2                                    # Stützstellenanzahl pro Richtung
xii =   [-1/np.sqrt(3), 1/np.sqrt(3)]        # Stützstellen-Koordinaten in xi
etai    =   [-1/np.sqrt(3), 1/np.sqrt(3)]    # Stützstellen-Koordinaten in eta
lambdai =   [1, 1]                           # Wichtungsfaktoren
assert (len(xii) == n and len(etai) == n and len(lambdai) == n), 'Falsche Vorgaben für die numerische Integration'

####### Aufgabenteil 1 ########################################################
    
## Steifigkeitsmatrix in Voigt-Notation:
C   =   E/(1-nu**2) * Matrix([[1, nu, 0], [nu, 1, 0], [0, 0, (1-nu)/2]])    

####### Aufgabenteil 2 ########################################################
    
## Bilineare Ansatzfunktionen auf dem Referenzelement: 
xi  =   sym.Symbol('xi')
eta =   sym.Symbol('eta')
N1  =   1/4 * (1-xi) * (1-eta)
N2  =   1/4 * (1+xi) * (1-eta)
N3  =   1/4 * (1+xi) * (1+eta)
N4  =   1/4 * (1-xi) * (1+eta)

N   =   Matrix([[N1, 0, N2, 0, N3, 0, N4, 0], [0, N1, 0, N2, 0, N3, 0, N4]])

## M-Matrix für bilineare Ansatzfunktion: 
M   =   zeros(2, 4)
M[0,:]  =   sym.diff(Matrix([[N1, N2, N3, N4]]), xi)
M[1,:]  =   sym.diff(Matrix([[N1, N2, N3, N4]]), eta)

J       =   []
detJ    =   []
invJ    =   []
for elem in range(e):
    # Jacobi-Matrix: 
    J.append(M * x[elem].row_join(y[elem]))
    
    # Determinante der Jacobi-Matrix: 
    detJ.append(J[elem].det())

    # Inverse der Jacobi-Matrix: 
    invJ.append(J[elem].inv())

####### Aufgabenteil 3 ########################################################

## Partitielle Ableitung der Ansatzfunktionen nach x und y:
partN    =   []
for elem in range(e):
    partN.append(sym.simplify(invJ[elem] * M))

## B-Matrix:
B   =   []
for elem in range(e):
    Ndx   =   partN[elem][0,:]
    Ndy   =   partN[elem][1,:]
    B.append(zeros(3, 8))
    B[elem][0,:]   =   Matrix([[Ndx[0], 0, Ndx[1], 0, Ndx[2], 0, Ndx[3], 0]])
    B[elem][1,:]   =   Matrix([[0, Ndy[0], 0, Ndy[1], 0, Ndy[2], 0, Ndy[3]]])
    B[elem][2,:]   =   Matrix([[Ndy[0], Ndx[0], Ndy[1], Ndx[1], Ndy[2], Ndx[2], Ndy[3], Ndx[3]]])

## Elementsteifigkeitsmatrix: 
Kelem   =   []
for elem in range(e):
    Kelem.append(zeros(8, 8))
    for i in range(n):
        for j in range(n):
            # B-Matrix an der Stelle:
            Bij =   B[elem].subs([(xi, xii[i]), (eta, etai[j])])
            # Determinante der Jacobi-Matrix an der Stelle: 
            detJij  =   detJ[elem].subs([(xi, xii[i]), (eta, etai[j])])
            # Berechnung der Elementsteifigkeitsmatrix:
            Kelem[elem]     =   Kelem[elem] + Bij.T * C * Bij * detJij * lambdai[i] * lambdai[j]

###### Aufgabenteil 4 #########################################################

## Zuordnungsmatrix:
# siehe Defintion in den Eingangsdaten

## Gesamtsteifigkeitsmatrix:
K   =   zeros(numdf, numdf)
for elem in range(e):
    K   =   K + L[elem].T * Kelem[elem] * L[elem]

###### Aufgabenteil 5 #########################################################
    
## Partitionierung:
# siehe Defintion in den Eingangsdaten

# Reduzierte Steifigkeitsmatrix:
KFF =   LF.T * K * LF

## Elementlastvektor:
felem   =   []
for elem in range(e):
    felem.append(zeros(8, 1))
    # Streckenlasten auf dem Rand:
    for Rand in range(4):
        for i in range(n):
            # Länge des Randes li und Ansatzfunktion des Randes Ni:
            if Rand == 0:
                li = sqrt((x[elem][1]-x[elem][0])**2+(y[elem][1]-y[elem][0])**2)
                Ni  =   N.subs([(xi, xii[i]), (eta, -1)])
            elif Rand == 1:
                li = sqrt((x[elem][2]-x[elem][1])**2+(y[elem][2]-y[elem][1])**2)
                Ni  =   N.subs([(xi, 1), (eta, etai[i])])
            elif Rand == 2:
                li = sqrt((x[elem][3]-x[elem][2])**2+(y[elem][3]-y[elem][2])**2)
                Ni  =   N.subs([(xi, xii[i]), (eta, 1)])
            else:
                li = sqrt((x[elem][0]-x[elem][3])**2+(y[elem][0]-y[elem][3])**2)
                Ni  =   N.subs([(xi, -1), (eta, etai[i])])
            # Berechnung des Elementlastvektors:
            felem[elem] =   felem[elem] + Ni.T * lambdai[i]  * tStrecken[elem][Rand,:].T * li/2
    # Knotenlasten:
    felem[elem] =   felem[elem] + tKnoten[elem]
    
## Gesamtlastvektor:
f   =   zeros(numdf, 1)
for elem in range(e):
    f   =   f + L[elem].T * felem[elem] 
    
## Reduzierter Lastvektor:
fFF =   LF.T * f

###### Aufgabenteil 6 #########################################################

## Lösen des linearen Gleichungssytems:
dF  =   np.linalg.solve(np.array(KFF, dtype=float), np.array(fFF, dtype=float))
d   =   LF * dF

print(d)