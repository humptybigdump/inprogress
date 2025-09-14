#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 21:02:28 2020

@author: Alexander Stroh
"""

import numpy as np
import matplotlib.pyplot as plt

# Konstanten
kappa=10
L=10
nodes=20
T_w=50
delta_x=L/(nodes-1)
x=np.linspace(0,L,nodes)

# Koeffizientenmatrix
A=np.zeros([nodes,nodes])

# Q-Vektor

Q=np.zeros([nodes,1])

w=np.zeros([nodes,1])
w[int(nodes/3):int(2*nodes/3)]=20

# innere Stützstellen
for i in range(1,nodes-1):
    # Koeffizientenmatrix
    A[i,i]=2
    A[i,i-1]=-1
    A[i,i+1]=-1
    # Q Vektor
    Q[i]=w[i]*delta_x**2/kappa

# Randwerte
A[0,0]=1
Q[0]=T_w

A[-1,-1]=1
A[-1,-2]=-1
Q[-1]=0

T=np.linalg.solve(A, Q)

plt.plot(x,w)
plt.plot(x,T)