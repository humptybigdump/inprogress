# -*- coding: utf-8 -*-
"""
Modeling of Reactions
Exercise 6
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.linalg import expm

# -----------------------------------------------------------------------------
# Exercise 6: Gas–Water Transfer with Decay
# -----------------------------------------------------------------------------

# Parameters
H = 2                # Henry's law coefficient [-]
Vw = 1e-3            # volume of water [m³]
Vg = 1e-3            # volume of gas [m³]
vwg = 1e-3 / 60      # gas-transfer velocity [m/s]
Awg = 0.01           # interfacial area [m²]
kmt = vwg * Awg / Vw # rate coefficient [1/s]

print(f'rate coeff. of gas transfer in the aqueous phase: {kmt:.6g}/s\n')

kdecvec = [0, 1/86400, 1/3600, 1/60, 1]  # decay coefficients [1/s]

# Plot setup
fig, axs = plt.subplots(2, 3, figsize=(15, 8))
axs = axs.flatten()

# Time settings
dt = 60               # [s]
nt = 1440             # number of time steps
time_array = np.arange(1, nt+1) * dt
t_hours = time_array / 3600  # time in hours

# Loop over decay coefficients
for ii, kdec in enumerate(kdecvec):
    print(f'kdec = {kdec:.6g}/s, kdec/kmt = {kdec/kmt:.6g}')

    # Coefficient matrix A [1/s]
    A = np.array([
        [-kmt - kdec, +kmt / H],
        [kmt * Vw / Vg, -kmt * Vw / (Vg * H)]
    ])
    print('A =\n', A)

    # Eigenanalysis
    eigvals, eigvecs = np.linalg.eig(A)
    print(f'1st eigenvector: [{eigvecs[0,0]:.4g}, {eigvecs[1,0]:.4g}]; eigenvalue: {eigvals[0]:.4g}/s')
    print(f'2nd eigenvector: [{eigvecs[0,1]:.4g}, {eigvecs[1,1]:.4g}]; eigenvalue: {eigvals[1]:.4g}/s\n')

    # Initial condition: all in gas phase
    c0 = np.array([0.0, 1.0])
    cmat = np.zeros((2, nt))

    # Analytical solution
    for i in range(nt):
        t = (i + 1) * dt
        cmat[:, i] = expm(A * t) @ c0

    # Plot analytical solution
    ax = axs[ii]
    ax.plot(t_hours, cmat[0, :],'r',label='water')
    ax.plot(t_hours, cmat[1, :],'b',label='gas')
    ax.set_xlabel('t [h]')
    ax.set_ylabel('c / c$_g^{ini}$ [-]')
    ax.set_title('k$_{dec}$ = ' + f'{kdec:.3g}/s')
    ax.grid(True)

    # ODE system definition
    def lin_sys_ode(t, c):
        dc = np.zeros_like(c)
        dc[0] = kmt * (c[1] / H - c[0]) - kdec * c[0]
        dc[1] = kmt * Vw / Vg * (c[0] - c[1] / H)
        return dc

    # Solve ODE numerically
    tspan = (0, nt * dt)
    t_eval = time_array
    sol = solve_ivp(lin_sys_ode, tspan, c0, method='BDF')

    # Plot numerical solution
    ax.plot(sol.t / 3600, sol.y[0],'rx',linewidth=0.5,label='water ODE')
    ax.plot(sol.t / 3600, sol.y[1],'bx',linewidth=0.5,label='gas ODE')

    ax.legend()

# Hide any unused subplot
for j in range(len(kdecvec), len(axs)):
    fig.delaxes(axs[j])

plt.tight_layout()
plt.show()
