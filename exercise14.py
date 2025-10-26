"""
Modeling of Reactions Excercise 14
Electron-Acceptor Chain
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
gamma = np.array([1, 0.8, 0.5, 0.5])           # Stoichiometric coefficients
rmax  = np.array([0.6, 0.4, 0.3, 0.2])         # DOC-decay rate coefficients
K     = np.array([0.016, 0.16, 0.005, 0.011])  # Michaelis-Menten constants
I     = np.array([3e-3, 4e-3, 6e-3])           # Inhibition constants

# Initial concentrations: [O2, NO3, SO4, DOC, CH4]
c0 = [0.25, 0.8, 2, 10, 0]
t_span = (0, 50)

def myode(t, c, gamma, rmax, K, I):
    # concentrations [mmol/L]
    c_DO, c_nit, c_sul, c_DOC, c_CH4 = c
    # Stoichiometry TEA:DOC [-]
    gamma_DO, gamma_nit, gamma_sul, gamma_CH4 = gamma
    # rate coefficient for different TEA [1/d]
    rmax_DO, rmax_nit, rmax_sul, rmax_DOC = rmax
    # Michaelis-Menten coefficient of the TEAs [mmol/l]
    K_DO, K_nit, K_sul, K_DOC = K
    # Inhibition constant of the TEAs [mmol/L]
    I_DO, I_nit, I_sul = I

    # Reaction rate terms
    # MiMen term of DOC
    fDOC = c_DOC / (c_DOC + K_DOC)
    # inhibition terms
    fI_DO = I_DO / (c_DO + I_DO)
    fI_nit = I_nit / (c_nit + I_nit)
    fI_sul = I_sul / (c_sul + I_sul)
    # now the combined reaction rates
    r_DO  = rmax_DO  * fDOC * c_DO  / (c_DO  + K_DO)
    r_nit = rmax_nit * fDOC * c_nit / (c_nit + K_nit) * fI_DO
    r_sul = rmax_sul * fDOC * c_sul / (c_sul + K_sul) * fI_DO * fI_nit
    r_DOC = rmax_DOC * fDOC * fI_DO * fI_nit * fI_sul

    # rates of change of concentration [mmol/l/d]
    dcdt = np.zeros_like(c)
    dcdt[0] = -gamma_DO * r_DO              # dissolved oxygen
    dcdt[1] = -gamma_nit * r_nit            # nitrate
    dcdt[2] = -gamma_sul * r_sul            # sulfate
    dcdt[3] = -r_DOC - r_DO - r_nit - r_sul # DOC
    dcdt[4] = gamma_CH4 * r_DOC             # methane
    return dcdt

# === Solve the ODE ===
sol = solve_ivp(myode, t_span, c0, args=(gamma, rmax, K, I), method='BDF')

T = sol.t
C = sol.y.T

# === Postprocess Reaction Rates ===
R = np.zeros((len(T), 4))
for i, t in enumerate(T):
    dcdt = myode(t, C[i, :], gamma, rmax, K, I)
    R[i, 0] = -dcdt[0] / gamma[0]
    R[i, 1] = -dcdt[1] / gamma[1]
    R[i, 2] = -dcdt[2] / gamma[2]
    R[i, 3] =  dcdt[4] / gamma[3]

# === Plotting ===
fig, axs = plt.subplots(1, 2, figsize=(14, 5))

# === First subplot: Concentrations with dual y-axis ===
axs[0].set_title('Concentrations')
axs[0].set_xlabel('t [d]')
axs[0].set_ylabel('c [mmol/L] (O$_2$, NO$_3^-$, SO$_4^{2-}$, CH$_4$)')

# concentrations belong to left axis: O2, NO3, SO4, CH4
h1, = axs[0].plot(T, C[:, 0], label='O$_2$')
h2, = axs[0].plot(T, C[:, 1], label='NO$_3^-$')
h3, = axs[0].plot(T, C[:, 2], label='SO$_4^{2-}$')
h5, = axs[0].plot(T, C[:, 4], label='CH$_4$')

# concentration belonging to right axis: DOC
ax_right = axs[0].twinx()
ax_right.set_ylabel('c [mmol/L] (DOC)')
  # different style for distinction
h4, = ax_right.plot(T, C[:, 3], 'k--', label='DOC')

# Combine legends from both y-axes
lines = [h1, h2, h3, h4, h5]
labels = [line.get_label() for line in lines]
axs[0].legend(lines, labels, title='Compound')

# === Second subplot: DOC Reaction Rates ===
axs[1].set_title('Reaction Rates of DOC as e$^-$-Donor')
axs[1].set_xlabel('t [d]')
axs[1].set_ylabel('r$_{DOC}^{(i)}$ [mmol/L/d]')
# remark: the methanogenesis rate is multiplied by 0.5 because half of the DOC
# involved is used as electron acceptor
axs[1].plot(T, R*np.array([1,1,1,0.5]))
axs[1].legend(['O$_2$', 'NO$_3^-$', 'SO$_4^{2-}$', 'DOC'], title='TEA')

plt.tight_layout()
plt.show()