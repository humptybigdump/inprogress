"""
Modeling of Reactions
Exercise 3: Freundlich sorption
s = K * c^n
m = Vw*c + ms*s = (Vw + ms*K*c^(n-1)) * c
"""

import numpy as np
import time


# Constants
n_Fr  = 0.7
K_Fr  = 2          # [mol^.3m^2.1/kg]
rho_s = 2650       # [kg/m3]
poros = 0.4

# Tolerance for mass balance
tol = 1e-7

# Mass of solids and volume of water in 1 m³ of bulk volume
ms = rho_s * (1 - poros)
Vw = poros

# Initial conditions
c0 = 10  # [mol/m³]
s0 = 0   # [mol/kg]
m  = Vw * c0 + ms * s0  # total mass [mol]

# -------------------------------
# Picard Iteration
# -------------------------------
print("Solve equilibration using Picard iteration")

c = c0
s = K_Fr * c**n_Fr
m_error = m - Vw * c - ms * s
iter_count = 0

while abs(m_error) > tol * m:
    iter_count += 1
    c = m / (Vw + ms * K_Fr * c**(n_Fr - 1))
    s = K_Fr * c**n_Fr
    m_error = m - Vw * c - ms * s
    print(f"iteration {iter_count:2d}: c = {c:8.3g} mol/m³, error = {m_error:8.3g} mol")

print(f"sorbing-phase concentration {s:.6g} mol/kg")

# -------------------------------
# Newton Iteration
# -------------------------------
print("Solve equilibration using Newton iteration")

c = c0
iter_count = 0
s = K_Fr * c**n_Fr
res = m - Vw * c - ms * s

while abs(res) > tol * m:
    iter_count += 1
    dresdc = -Vw - ms * K_Fr * n_Fr * c**(n_Fr - 1)
    dc = -res / dresdc

    # Line search to keep concentration non-negative
    fac = 1.0
    while c + fac * dc < 0:
        fac *= 0.9

    c += fac * dc
    s = K_Fr * c**n_Fr
    res = m - Vw * c - ms * s
    print(f"iteration {iter_count:2d}: c = {c:8.3g} mol/m³, error = {res:8.3g} mol")

print(f"sorbing-phase concentration {s:.6g} mol/kg")
