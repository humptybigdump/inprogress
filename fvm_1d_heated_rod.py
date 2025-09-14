#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 13:46:41 2025

@author: ensm_student
"""


import numpy as np
import matplotlib.pyplot as plt


def main():
    
    # Constants
    kappa = 10
    L = 10
    T0 = 50
    
    # Discretisation
    cells = 10
    dx = L / cells
    x = np.linspace(dx/2, L - dx/2, cells)
    
    global A, Q, w, T
    w = np.zeros([cells, 1])
    w[cells//2:cells] = 10
    
    # A*x = Q
    A = np.zeros([cells, cells])
    Q = np.zeros([cells, 1])
    
    # Gleichung:
    # 2 T_P - T_E - T_W = w_P * dx**2 / kappa
    for i in range(1, cells - 1):
        A[i,i] = 2
        A[i,i-1] = -1
        A[i,i+1] = -1
        Q[i] = w[i] * dx**2 / kappa

    # Randbedingungen:
    # 3 T_P - T_E = w_P * dx**2 / kappa + 2*T0
    A[0,0] = 3
    A[0,1] = -1
    Q[0] = w[0] * dx**2 / kappa + 2*T0
    #A[0,0] = 1
    #A[0, 1] = -1
    #Q[0] = w[0] * dx**2 / kappa
    
    
    # T_P - T_E = w_P * dx**2 / kappa
    A[-1,-1] = 1
    A[-1,-2] = -1
    Q[-1] = w[-1] * dx**2 / kappa
    
    T = np.linalg.solve(A, Q)
    
    plt.figure()
    plt.plot(x, T, label="T")
    plt.plot(x, w, label="w")
    plt.legend()
    plt.grid()
        
    plt.figure()
    plt.spy(A)

if __name__ == "__main__":
    main()


