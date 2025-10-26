"""
Modeling of Reactions
Exercise 16
Istope Fractionation of Phenol in a Pond
"""
# Computes the concentration of phenol and its isotopes in a pond
# considering Monod-kinetics of microbial degradation and associated
# biomass growth, and dilution. Oxygen is available in excess.
# t: time [d]
# c: concentrations
#    1: conservative tracer [mol/m3]
#    2: isotopically light phenol [mol/m3]
#    3: isotopically heavy phenol [mol/m3]
#    4: biomass [g/m3]
# par: parameters
#    1: mean residence time in the pond [d]
#    2: maximum specific growth rate for turnover of light isotopologe [1/d]
#    3: maximum specific growth rate for turnover of heavy isotopologe [1/d]
#    4: Monod coefficient for light isotopologe [mol/m3]
#    5: Monod coefficient for heavy isotopologe [mol/m3]
#    6: yield coefficient [g/mol]
#    7: biomass decay coefficient [1/d]

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def isotope_lake_ode(t, c, par):
    dcdt = np.zeros_like(c)
    tracer, C12, C13, bio = c
    T, mumax12, mumax13, K12, K13, Y, kdec = par

    # growth rate of biomass by degrading light phenol
    growth12 = mumax12 * C12 / K12 / (1 + C12/K12 + C13/K13) * bio
    # growth rate of biomass by degrading heavy phenol
    growth13 = mumax13 * C13 / K13 / (1 + C12/K12 + C13/K13) * bio

    # rates of change of concentration
    dcdt[0] = -tracer / T                      # tracer: only dilution
    dcdt[1] = -C12 / T - growth12 / Y          # C12-phenol: dilution and decay
    dcdt[2] = -C13 / T - growth13 / Y          # C13-phenol: dilution and decay
    dcdt[3] = growth12 + growth13 - (kdec + 1/T) * bio  # Biomass: dilution, growth and decay
    return dcdt

# Assumption on fractionation:
epsilon = -2e-3          # fractionation coefficient [-]
alpha = 1 + epsilon      # fractionation factor [-]

# Standard isotope ratio
C13C12_ref = 0.0111802
# initial delta-value
delta0 = -23e-3
# initial isotope ratio
C13C12_0 = (delta0 + 1) * C13C12_ref

# Parameters
T = 432 / 1e-3 / 86400  # mean residence time [d]
mumax12 = 1             # max growth rate for light isotope [1/d]
mumax13 = alpha * mumax12
K12 = 0.1               # Monod coefficient [mol/m3]
K13 = K12
Y = 10                  # yield coefficient [g/mol]
kdec = 0.1              # biomass decay coefficient [1/d]
par = [T, mumax12, mumax13, K12, K13, Y, kdec]

# Initial concentrations
Cini = 80000 / 94 / 432   # total concentration [mol/m3]
C12_0 = Cini / (1 + C13C12_0)
C13_0 = Cini * C13C12_0 / (1 + C13C12_0)
bio_0 = 1e-2              # [g/m3]
c0 = [Cini, C12_0, C13_0, bio_0]

# Time span
tspan = (0, 10)
t_eval = np.linspace(*tspan, 300)

# Solve ODE
sol = solve_ivp(isotope_lake_ode, tspan, c0, args=(par,), method='BDF', t_eval=t_eval)
t, c = sol.t, sol.y.T

# Postprocessing
tracer = c[:, 0]                    # [mol/m3]
ctot = c[:, 1] + c[:, 2]            # total phenol [mol/m3]
relconc = ctot / tracer             # normalized concentration [-]
Delta = c[:, 2] / c[:, 1] / C13C12_ref - 1

# Plotting
fig1, axs = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)
axs[0].plot(t, tracer, label='tracer')
axs[0].plot(t, ctot, label='phenol')
axs[0].set_ylabel('c [mol/m$^3$]')
axs[0].set_xlabel('t [d]')
axs[0].legend()
axs[0].set_title('Concentrations of Solutes')

axs[1].plot(t, Delta * 1000)
axs[1].set_ylabel(r'$\delta^{13}C$ [‰]')
axs[1].set_xlabel('t [d]')
axs[1].set_title(r'$\delta^{13}C$ of Phenol')

axs[2].plot(t, c[:, 3])
axs[2].set_ylabel('c$_{bio}$ [g/m$^3$]')
axs[2].set_xlabel('t [d]')
axs[2].set_title('Biomass Concentration')
fig1.suptitle('Time Series')

fig2, axs2 = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
axs2[0].semilogx(ctot / Cini, Delta * 1000)
axs2[0].set_xlabel('c(t)/c(0) [-]')
axs2[0].set_ylabel(r'$\delta^{13}C$ [‰]')
axs2[0].set_title(r'$\delta^{13}C$ as Function of c')
axs2[0].grid(True, which='both')

rayleigh = (np.log(relconc) * epsilon + delta0) * 1000
axs2[1].semilogx(relconc, Delta * 1000, 'x', label='Simulation')
axs2[1].semilogx(relconc, rayleigh, '-', label='Rayleigh equation')
axs2[1].set_xlabel('c(t)/c$_{cons}$ [-]')
axs2[1].set_ylabel(r'$\delta^{13}C$ [‰]')
axs2[1].legend()
axs2[1].set_title('Rayleigh Plot')
axs2[1].grid(True, which='both')
fig2.suptitle('Isotope Ratios')

plt.show()
