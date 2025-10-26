"""
% =========================================================================
% 1-D Simulation of Solute Transport - Simple Version 
% Demo example with 2 compounds, one being conservative, the other undergoing
% first-order decay
%
% operator-split approach with
% 1) explicit Euler integration of advection
% 2) implicit Euler integration of dispersion
% 3) explicit Euler integration of reaction
%
% Olaf A. Cirpka
% University of Tübingen
% Department of Geosciences
% olaf.cirpka@uni-tuebingen.de
%
% Matlab version: June 19, 2024
% Python version: February 25, 2025
% =========================================================================
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib
matplotlib.use('QT5Agg')
from PyQt5.QtWidgets import QDesktopWidget
import matplotlib.pyplot as plt


# function to create a full-screen interactive window that fills the full screen
def fullscreenfigure(fignum):
    # open or create the figure with number fignum
    fig = plt.figure(fignum,figsize=(16, 9),dpi=72,clear=True,layout='constrained')
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


# =======================================================================================
# Define Coefficients
# =======================================================================================

# Transport Coefficients
L = 1              # length of column [m]
r = 0.05           # radius of column [m]
A = np.pi * r**2   # cross-sectional area [m2]
Q = 1e-4 / 60      # discharge 100 ml/min in m3/s
q = Q / A          # specific discharge [m/s]
poros = 0.4        # porosity [-]
alpha = 0.005      # dispersivity [m]
Dp = 1e-9          # pore diffusion coefficient [m2/s]
lam = 1e-3         # first-order decay coeff. [1/s]

tinj = 3600 * 1    # time of solute injection [s]
te = 3600 * 2      # end time [s]
t_output = 60      # time increment for graphical output [s]

# Derived Coefficients
v = q / poros      # seepage velocity [m/s]
D = alpha * v + Dp # dispersion coefficient [m2/s]
t_PV = L / v       # time for one pore volume [s]

# Spatial resolution
dx = 0.01          # [m]
dt = dx / v        # Ensures Courant-number of 1

# =======================================================================================
# Some Preparations
# =======================================================================================

# Spatial Discretization
x = np.arange(0.5 * dx, L + dx, dx)
# number of cells
nx = len(x)

# Dispersion Matrix
diag_main = np.ones(nx) * (1 + 2*D*dt/dx**2)
diag_lower = np.ones(nx - 1) * (-D*dt/dx**2)
diag_upper = np.ones(nx - 1) * (-D*dt/dx**2)
M = sp.diags([diag_lower, diag_main, diag_upper], [-1, 0, 1], format='csr')
# First Entry of Concentration is not Altered by Dispersion
M[0, 0], M[0, 1] = 1, 0
# No-Dispersive-Flux Boundary Condition at End f Domain
M[-1, -2], M[-1, -1] = -D * dt / dx**2, 1 + D * dt / dx**2

# =======================================================================================
# Initialization of Cooncentration Matrix
# =======================================================================================

# Number of Components
ncomp = 2

# names of the compounds
names = ['cons.', 'react.']

# Matrix of Initial Aqueous Concentrations [mmol/L]
if ncomp>1:
   c = np.zeros((nx, ncomp))
else:
   c = np.zeros(nx)

# Inflow Concentration [mmol/L]
# Note: Must be defined as an array even in the scalar case
c_in = np.array([1.0, 1.0]) # length must match ncomp
# c_in = np.array([1.0])
# Initialize Breakthrough Curves
BTC = []

t = 0

# Initialize graphical output
fig1 = fullscreenfigure(1)
ax = fig1.add_subplot()
ax.cla()
lines = ax.plot(x, c)
plt.xlabel('x [m]')
plt.ylabel('c [mmol/L]')
plt.ylim([0, 1.1])
titext = plt.title(f'Concentration, t={t / 3600:.1f}h')
plt.draw()
ax.legend(names)
plt.pause(0.2)
plt.show()

# =======================================================================================
# Time loop
# =======================================================================================
for t in np.arange(dt, te + dt, dt):
    # Inflow Concentration
    if ncomp > 1:
       c_inj = c_in if t < tinj else np.zeros((1,ncomp))
    else:
       c_inj = c_in if t < tinj else np.zeros(1)

    # Breakthrough Curve
    BTC.append(np.array(c[-1,:]) if c.ndim > 1 else np.array(c[-1]))
    
    # ===================================================================================
    # Advection (Explicit-Euler Integration with Courant-Number 1)
    # ===================================================================================
    if ncomp > 1:
       c[1:, :] = c[:-1, :]
       c[0, :] = c_inj
    else:
       c[1:] = c[:-1]
       c[0] = c_inj[0]
    
    # ===================================================================================
    # Dispersion (Implicit Euler)
    # ===================================================================================
    c = spla.spsolve(M, c, use_umfpack=True)
    
    # ===================================================================================
    # Reaction:
    # ===================================================================================
    # initialize reaction rates [mmol/L/s]
    if ncomp > 1:
       r = np.zeros((nx,ncomp))
    else:
       r = np.zeros(nx)
    # first compound is conservative, while second compound undergoes first-order decay
    r[:,1] = -c[:,1]*lam
    # add corresponding change of concentration [mol/L]
    c += r*dt 
    
    # ===================================================================================
    # Graphical output
    # ===================================================================================
    if t % t_output <= dt:
      # updating concentration values of the lines
      for i in range(ncomp):
          lines[i].set_ydata(c[:,i])
      # updating text of the title
      titext.set_text(f'Concentration, t={t / 3600:.1f}h')
      # drawing updated values
      fig1.canvas.draw()
      fig1.canvas.flush_events()
      plt.pause(0.1)
      plt.show()

# =======================================================================================
# Plot Breathrough Curves
# =======================================================================================

# Initialize graphical output
fig2 = fullscreenfigure(2)

plt.plot(np.arange(dt, te + dt, dt) / t_PV, np.array(BTC))
plt.ylim([0, 1.1])
plt.xlabel('PV [-]')
plt.ylabel('c [mmol/L]')
plt.title('Breakthrough Curve')
plt.legend(names)
plt.show(block=True)
