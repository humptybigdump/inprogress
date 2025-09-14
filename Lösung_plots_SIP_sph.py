#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 14:00:23 2025

@author: lukas
"""
import matplotlib.pyplot as plt
import numpy as np

K_M, G_M = 75.0, 25.0

K_E, G_E = 160.0, 80.0
# K_E, G_E = 0.001, 0.001

R = 1
eps_0 = 0.01

B = (K_M - K_E)/(K_E+4/3*G_M)
A = -B/R**3

r_M = np.linspace(R, 5, 200)
r_E = np.linspace(0, R, 50)

u_M = (1-A/r_M**3)*r_M*eps_0
u_E = (1+B)*r_E*eps_0

eps_E = (1+B)*eps_0*np.ones(r_E.size)
eps_M = eps_0+2 * A*eps_0/r_M**3

sig_E = 3*K_E*eps_E
sig_M = 3*K_M*eps_0+4*G_M * A*eps_0/r_M**3

r = np.append(r_E, r_M)
u = np.append(u_E, u_M)
eps = np.append(eps_E, eps_M)
sig = np.append(sig_E, sig_M)

plt.figure(figsize=(6, 4))
plt.plot(r, u)
plt.xlabel(r"$r$ in mm")
plt.ylabel(r"$u_r(r) $ in mm")
plt.title("Verschiebung in radialer Richtung")
plt.grid()
plt.savefig("SIP_sph_u.pdf")

plt.figure(figsize=(6, 4))
plt.plot(r, eps*100)
plt.xlabel(r"$r$ in mm")
plt.ylabel(r"$\varepsilon_{rr}(r)$ in %")
plt.title("Normaldehnung in radialer Richtung")
plt.grid()
plt.savefig("SIP_sph_eps.pdf")

plt.figure(figsize=(6, 4))
plt.plot(r, sig)
plt.xlabel(r"$r$ in mm")
plt.ylabel(r"$\sigma_{rr}(r)$ in GPa")
plt.title("Normalspannung in radialer Richtung")
plt.grid()
plt.savefig("SIP_sph_sig.pdf")
