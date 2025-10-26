# -*- coding: utf-8 -*-
"""
Modeling of Reactions
Exercise 5
"""

import numpy as np

# -------------------------------
# Multicomponent Sorption: Picard Iteration
# -------------------------------

# Parameters
Vtot = 10                      # total volume [L]
Vw = 0.75 * Vtot              # volume of water [L]
rho_s = 1.5                   # resin density [kg/L]
m_s = 0.25 * Vtot * rho_s     # mass of resin [kg]
s_max = 10                    # sorption capacity [mol/kg]
K = np.array([0.5, 5.0])      # half-saturation concentrations [mol/L]
tol = 1e-6                    # tolerated relative error [-]

# Initial concentrations [mol/L]
c_ini = np.array([1.0, 0.0])

# Initial sorbed-phase concentrations using Langmuir-like formula
s_ini = s_max * c_ini / K / (1 + np.sum(c_ini / K))

# Initial masses
m_ini_w = c_ini * Vw
m_ini_s = s_ini * m_s
m_ini = m_ini_w + m_ini_s

print(f"initial sorbing-phase conc.: {s_ini[0]:8.3g} mol/kg")
print(f"initial total mass:          {m_ini[0]:8.3g} mol")

# Reequilibration: new total masses
m_new = np.array([m_ini_s[0], Vw * 10])  # compound A: only sorbed, B: only in water

# Initial guess: all in water
c = m_new / Vw

# Initial values
mysum = 1 + np.sum(c / K)
s = s_max * c / (K * mysum)
m_error = m_new - c * Vw - s * m_s

# Picard iteration
iter_count = 0
while np.max(np.abs(m_error) / m_new) > tol:
    iter_count += 1
    c = m_new / (Vw + m_s * s_max / K / mysum)
    mysum = 1 + np.sum(c / K)
    s = s_max * c / (K * mysum)
    m_error = m_new - c * Vw - s * m_s

# Output
print("After reequilibration")
print(f"number of iterations {iter_count:2d}")
print(f"c = {c[0]:8.3g}, {c[1]:8.3g} mol/L")
print(f"s = {s[0]:8.3g}, {s[1]:8.3g} mol/kg")
print(f"mass-balance error = {m_error}")
