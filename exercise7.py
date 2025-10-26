"""
Modeling of Reactions, Micobial Dynamics, and Bioreactive Transport
Solution to Problems 5 & 7
Equilibrium and Kinetic Langmuir Sorption
(c) Olaf A. Cirpka, University of Tübingen, Department of Geosciences
March 2025
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('QT5Agg')
# from PyQt5.QtWidgets import QDesktopWidget

# =============================================================================
# Function, to open an interactive window, covering the entire screen
# =============================================================================
def fullscreenfigure(fignum):
    # open or create the figure with number fignum
    fig = plt.figure(fignum,figsize=(16, 9),dpi=72,clear=True,
                     layout='constrained')
    # clear figure
    fig.clf()
    # try to bring it to the front
    fig.canvas.manager.window.raise_()
    # enable interactive mode
    plt.ion()
    # Choose a font family (e.g., serif, sans-serif, etc.)
    plt.rcParams['font.family'] = 'sans-serif'
    # Set the specific font (e.g., Times New Roman)
    plt.rcParams['font.sans-serif'] = ['Arial']  
    # Set resolution
    plt.rcParams["figure.dpi"] = 400
    # Set font size
    plt.rcParams.update({'font.size':14})                 # fontsize 
    # make the window fill the entire screen
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    window = fig.canvas.manager.window.geometry()
    frame  = fig.canvas.manager.window.frameGeometry()
    dheight=frame.height()-window.height()
    fig.canvas.manager.window.setGeometry(1, dheight-1, screen_width-2, screen_height-dheight)
    return fig

# =============================================================================
# Exercsie 5: Equilibrium Langmuir Sorption
# =============================================================================

# Constants
Vtot = 0.01     # total volume [m3]
frac_w = 0.75   # fraction of water
rho_res = 1500. # density of resin [kg/m3]
s_max = 10.     # specific sorption capacity [mol/kg]
K_A = 500.      # half-saturation conc. A [mol/m3]
K_B = 5000.     # half-saturation conc. B [mol/m3]
c_A_ini = 1000. # initial concentration A [mol/m3]
c_B_inj = 1e4   # injected concentration B [mol/m3]

V_w = Vtot * frac_w                    # volume of water
m_res = Vtot * (1 - frac_w) * rho_res  # mass of the resin [kg]

# Question 1: Initial sorbed concentration and masses
s_A_ini = c_A_ini * s_max / (K_A + c_A_ini)
m_A_ini = s_A_ini * m_res + c_A_ini * V_w

print('Exercise 5, Answers to Question 1')
print(f'initial sorbed conc. A {s_A_ini:.3g} mol/kg')
print(f'initial total mass   A {m_A_ini:.3g} mol')

# Question 2: Reequilibration after replacing the aqueous solution
m_A = s_A_ini * m_res  # total mass of compound A 
m_B = V_w * c_B_inj  # total mass of compound B

print('\nGo on to Question 2')
print(f'total mass A {m_A} mol')
print(f'total mass B {m_B} mol')

# initial guess
c_A = 0
c_B = c_B_inj

c_A_old = c_A_ini
c_B_old = 0

iter_count = 0  # iteration index (only for curiosity)

# Picard iteration
while ((c_A - c_A_old) ** 2 + (c_B - c_B_old) ** 2 > 1e-5):
    iter_count += 1
    sum_ci_over_Ki = c_A / K_A + c_B / K_B
    c_A_old = c_A
    c_B_old = c_B
    c_A = m_A / (V_w + m_res * s_max / K_A / (1 + sum_ci_over_Ki))
    c_B = m_B / (V_w + m_res * s_max / K_B / (1 + sum_ci_over_Ki))

c_A_eq = np.copy(c_A)
c_B_eq = np.copy(c_B)

print(f'{iter_count} iterations needed to compute new equilibrium:')
print(f'c_A = {c_A_eq:.4g} mol/m3, c_B = {c_B_eq:.4g} mol/m3')

# Now compute the sorbed mass explicitly
sum_ci_over_Ki = c_A_eq / K_A + c_B_eq / K_B
s_A_eq = c_A_eq * s_max / K_A / (1 + sum_ci_over_Ki)
s_B_eq = c_B_eq * s_max / K_B / (1 + sum_ci_over_Ki)
print(f's_A = {s_A_eq:.4g} mol/kg, s_B = {s_B_eq:.4g} mol/kg')

# =============================================================================
# Exercise 7: Kinetic Mass Transfer
# =============================================================================
# ODE system
def myode(t, y, kmt_a, kmt_s, K_A, K_B, s_max):
    c_A, s_A, c_B, s_B = y
    s_free = s_max - s_A - s_B
    dcA_dt = kmt_a[0] * (s_A - c_A / K_A * s_free)
    dsA_dt = kmt_s[0] * (c_A / K_A * s_free - s_A)
    dcB_dt = kmt_a[1] * (s_B - c_B / K_B * s_free)
    dsB_dt = kmt_s[1] * (c_B / K_B * s_free - s_B)
    return [dcA_dt, dsA_dt, dcB_dt, dsB_dt]

print('\nExercise 7, kinetic mass transfer')
# mass transfer coefficient as seen from the sorbing phase
kmt_s = [1, 2]  # [1/h]
# mass transfer coefficient as seen from the aqueous phase
kmt_a = [kmt_s[i] * m_res / V_w for i in range(2)]  # [kg/m3/h]
# time span
tspan = [0, 4 * max([1 / kmt_a[0], 1 / kmt_s[0], 1 / kmt_a[1], 1 / kmt_s[1]])]
# initial condition
C0 = [0, s_A_ini, c_B_inj, 0]

# solve ODE system
sol = solve_ivp(myode, tspan, C0, args=(kmt_a, kmt_s, K_A, K_B, s_max), 
                method='BDF')

T = sol.t
C = sol.y.T

# time to reach 99% of equilibrium
t_99_A = np.interp(0.99, 1.-(C[:,0] - C[-1,0]) / (C[0,0] - C[-1,0]), T)
t_99_B = np.interp(0.99, 1.-(C[:,2] - C[-1,2]) / (C[0,2] - C[-1,2]), T)
print(f'99% equilibration of compound A after {t_99_A:.3f}h')
print(f'99% equilibration of compound B after {t_99_B:.3f}h')

# graphical output
# fig1 = fullscreenfigure(1)
ax = plt.subplot(1, 1, 1)
line1, = plt.plot(T, C[:, 0],label='c$_A$')
line2, = plt.plot(T, C[:, 2],label='c$_B$')
plt.ylabel('c [mol/m$^3$]')
plt.xlabel('t [h]')
plt.plot(tspan[1],c_A_eq,'xk')
plt.plot(tspan[1],c_B_eq,'xk')
plt.axvline(x=t_99_A, color='k', linestyle=':')
plt.axvline(x=t_99_B, color='k', linestyle='-.')
ax.set_xlim([0, tspan[-1]])
ax.set_ylim([0, c_B_inj])

ax2 = ax.twinx()
line3, = plt.plot(T, C[:, 1],label='s$_A$',linestyle='--')
line4, = plt.plot(T, C[:, 3],label='s$_B$',linestyle='--')
plt.ylabel('s [mol/kg]')
plt.xlabel('t [h]')
ax2.set_ylim([0, s_A_ini])
plt.plot(tspan[1],s_A_eq,'xk')
line5, = plt.plot(tspan[1],s_B_eq,'xk',label='equilibrium')

# Combine legends
lines = [line1, line2, line3, line4, line5]
labels = [line.get_label() for line in lines]
ax2.legend(lines, labels)

plt.title('Kinetic Mass Transfer of Competing Sorbents on a Resin')
# plt.show(block=True)
plt.show()
