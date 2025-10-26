# -*- coding: utf-8 -*-
"""
Modeling of Reactions
Exercise 15
Compute reductive complete dechlorination of PCE
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# === Parameters ===
# order of concentrations: PCE, TCE, DCE, VC, ETH, EtOH
r_max = np.array([200, 100, 100, 50])  # [umol/L/d]
K_CE = np.array([0.4, 1, 1, 3])        # [umol/L]
K_EtOH = 150                           # [umol/L]
c0 = [200, 0, 0, 0, 0, 400]            # Initial concentrations 

tspan = np.arange(0, 30.1, 0.1)

# === ODE Function ===
def myode(t, c, r_max, K_CE, K_EtOH, is_competitive):
    dcdt = np.zeros_like(c)
    # concentrations [umol/L]
    # 0: PCE, 1: TCE, 2: DCE, 3: VC, 4: ETH, 5: EtOH
    c_PCE, c_TCE, c_DCE, c_VC, c_ETH, c_EtOH = c
    # half-velcoiyt concentrations [umol/l]
    K_PCE, K_TCE, K_DCE, K_VC = K_CE
    # maximum reaction rates [umol/l/d]
    r_max_PCE, r_max_TCE, r_max_DCE, r_max_VC = r_max

    if is_competitive:
        # common factor in the denominator
        denom = 1 + c_PCE/K_PCE + c_TCE/K_TCE + c_DCE/K_DCE + c_VC/K_VC
        # common factor for all rate constants
        common = c_EtOH / (K_EtOH + c_EtOH) / denom
        # individual reaction rates
        r_PCE = r_max_PCE * c_PCE / K_PCE * common
        r_TCE = r_max_TCE * c_TCE / K_TCE * common
        r_DCE = r_max_DCE * c_DCE / K_DCE * common
        r_VC  = r_max_VC  * c_VC  / K_VC  * common
    else:
        # common factor related to the electron donor
        EtOH_term = c_EtOH / (K_EtOH + c_EtOH)
        # individual reaction rates
        r_PCE = r_max_PCE * EtOH_term * c_PCE / (c_PCE + K_PCE)
        r_TCE = r_max_TCE * EtOH_term * c_TCE / (c_TCE + K_TCE)
        r_DCE = r_max_DCE * EtOH_term * c_DCE / (c_DCE + K_DCE)
        r_VC  = r_max_VC  * EtOH_term * c_VC  / (c_VC  + K_VC)

    # now evaluate the rates of change of concnetration
    dcdt[0] = -r_PCE
    dcdt[1] = +r_PCE - r_TCE
    dcdt[2] = +r_TCE - r_DCE
    dcdt[3] = +r_DCE - r_VC
    dcdt[4] = +r_VC
    dcdt[5] = -0.5 * (r_PCE + r_TCE + r_DCE + r_VC)

    return dcdt

# === Solve ODE ===
sol_non  = solve_ivp(myode, [tspan[0], tspan[-1]], 
                     c0, args=(r_max, K_CE, K_EtOH, False), 
                     t_eval=tspan, method='BDF')
sol_comp = solve_ivp(myode, [tspan[0], tspan[-1]], 
                     c0, args=(r_max, K_CE, K_EtOH, True), 
                     t_eval=tspan, method='BDF')

# === Plotting ===
fig, axs = plt.subplots(1, 2, figsize=(14, 5))
species = ['PCE', 'TCE', 'DCE', 'VC', 'ETH', 'EtOH']

axs[0].set_title('Without Competitive Inhibition')
axs[0].set_xlabel('t [d]')
axs[0].set_ylabel('c [μmol/L]')
for i in range(6):
    axs[0].plot(sol_non.t, sol_non.y[i], label=species[i])
axs[0].legend()

axs[1].set_title('With Competitive Inhibition')
axs[1].set_xlabel('t [d]')
axs[1].set_ylabel('c [μmol/L]')
for i in range(6):
    axs[1].plot(sol_comp.t, sol_comp.y[i], label=species[i])
axs[1].legend()

plt.tight_layout()
plt.show()
