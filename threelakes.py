"""
Modeling of Reactions, Micobial Dynamics, and Bioreactive Transport
Solution to Problem 2
Sulfate in Three Lakes in Series
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
# Part 1 (prior to remediation)
# =============================================================================

# Constants
V = np.array([1000., 500., 1700.])  # volumes [m3]
Q = 500.                            # discharge [m3/s]
lambda_ = np.array([0.1, 2, 0.01])  # first-order decay coefficients [1/d]
cin = 1000.                         # concentration in the inflow [mg/L = g/m3]

print('Part 1: Prior to Remediation')

# 1a: Residence times
tau = V / Q
for ii in range(3):
    print(f'residence time of lake {ii + 1}: {tau[ii]} d')

# 1b: ODE system
def lakeode(t, c, lambda_, tau, cin):
    dcdt = np.zeros_like(c)
    dcdt[0] = -lambda_[0] * c[0] + (cin - c[0]) / tau[0]
    dcdt[1] = -lambda_[1] * c[1] + (c[0] - c[1]) / tau[1]
    dcdt[2] = -lambda_[2] * c[2] + (c[1] - c[2]) / tau[2]
    return dcdt

# coefficient matrix and inhomogeneous term for dc/dt = K*c + s
K = np.array([
    [-lambda_[0] - 1/tau[0], 0, 0],
    [1/tau[1], -lambda_[1] - 1/tau[1], 0],
    [0, 1/tau[2], -lambda_[2] - 1/tau[2]]
])
s = np.array([cin/tau[0], 0, 0])
c0 = np.zeros(3)

# solve ODE system
sol = solve_ivp(lakeode, [0, 35], c0, args=(lambda_, tau, cin), 
                method='BDF')
T = sol.t
C = sol.y.T

# fig1 = fullscreenfigure(1)
lines = plt.plot(T, C)
plt.xlabel('t [d]')
plt.ylabel('c [mg/L]')

# 1c: steady-state concentrations
c_ss = np.linalg.solve(-K, s)
for ii in range(3):
    print(f'steady-state conc. in lake {ii + 1}: {c_ss[ii]:.3g} mg/L')

plt.axhline(y=c_ss[0], color=lines[0].get_color(), linestyle=':')
plt.axhline(y=c_ss[1], color=lines[1].get_color(), linestyle=':')
plt.axhline(y=c_ss[2], color=lines[2].get_color(), linestyle=':')
plt.legend(['lake 1', 'lake 2', 'lake 3','equilibrium'])

plt.gca().set_xlim([0,35])
plt.gca().set_ylim([0,900])

plt.title('Concentrations prior to Remediation')
plt.show()

# =============================================================================
# Part 2: With remediation in the inflow
# =============================================================================
print('Part 2: With Remediation in the Inflow')

# compute first-order decay coeff in the inflow
# exp(-kin*1day) = 0.925
kin = -np.log(0.925)  # [1/d]

# new ODE system
def lakeode_new(t, c, lambda_, tau, cin, kin):
    dcdt = np.zeros_like(c)
    cin_new = cin * np.exp(-kin * t)
    dcdt[0] = -lambda_[0] * c[0] + (cin_new - c[0]) / tau[0]
    dcdt[1] = -lambda_[1] * c[1] + (c[0] - c[1]) / tau[1]
    dcdt[2] = -lambda_[2] * c[2] + (c[1] - c[2]) / tau[2]
    return dcdt

# solve ODE system
sol_new = solve_ivp(lakeode_new, [0, 35], c_ss, 
                    args=(lambda_, tau, cin, kin), method='BDF')
Tnew = sol_new.t
Cnew = sol_new.y.T

cin_new = cin * np.exp(-kin * Tnew)

# fig2 = fullscreenfigure(2)
lines = plt.plot(Tnew, np.column_stack((cin_new, Cnew)))
plt.xlabel('t [d]')
plt.ylabel('c [mg/L]')
plt.legend(['inflow', 'lake 1', 'lake 2', 'lake 3'], loc='best')
plt.title('Concentrations upon Onset of Remediation')

# time to reach target concentration
c_std = 250
t_rem = np.zeros(3)

for ii in range(3):
    t_rem[ii] = np.interp(c_std, Cnew[::-1, ii], Tnew[::-1])
    print(f'time to reach {c_std} mg/L in lake {ii + 1}: {t_rem[ii]:.3g} d')

plt.gca().set_xlim([0,35])
plt.gca().set_ylim([0,1000])
plt.axvline(x=t_rem[0], color=lines[1].get_color(), linestyle=':')
plt.axvline(x=t_rem[1], color=lines[2].get_color(), linestyle=':')
plt.axvline(x=t_rem[2], color=lines[3].get_color(), linestyle=':')
plt.axhline(y=c_std, color='k', linestyle=':')

# plt.show(block=True)
plt.show()
