"""
Generic reactive transport model
1-D ADE coupled to reactions using the global implicit coupling approach

On the internal numbering
n_mob and n_imm are the numbers of mobile and immobile compounds
n_comp is the total number of compounds
n_cells is the number of cells
c[1::n_comp] is the vector of concentrations of the first compound in all cells
c[2::n_comp] is the vector of concentrations of the second compound in all cells
and so forth

Note: The first n_mob compounds are the mobile compounds
c[(ix-1)*n_comp+1:ix*c_comp is the vector of all concentrations within cell ix

Created on Thu Feb 13 2025

@author: Olaf A. Cirpka, University of Tuebingen, Department of Geosciences
"""

import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
from PyQt5.QtWidgets import QDesktopWidget
import matplotlib.pyplot as plt
from scipy.integrate import BDF
import scipy.sparse as sp
 
# =============================================================================
# DEFINITION OF THE ODE-SYSTEM FOR REACTIVE TRANSPORT
# =============================================================================
def ode_transport(t, c):
    # some of the parameter passed to ode-transport are only needed in the
    # plotting function plot_profile
    
    # initialize rate of change of concentrations
    dcdt = np.zeros_like(c)

    # loop over all mobile compounds
    for ic in range(n_mob):
        # extract vector of compound ic in all cells
        cvec = c[ic::n_comp]
        # spatial derivative
        gradc = np.diff(cvec) / dx
        # advection
        if TVD:
            # extend the concentration vector :
            cext = np.concatenate(([c_in[ic]], cvec, cvec[-1:]))
            s_1 = np.concatenate([np.diff(cext) / dx, [0]])
            s_2 = np.concatenate([[0], np.diff(cext) / dx])
            s = np.zeros_like(s_1)
            # van Leer limiter
            mask = s_1 * s_2 > 0
            s[mask] = 2 * s_1[mask] * s_2[mask] / (s_1[mask] + s_2[mask])
            # now construct concentration at interface
            c_up = cext[:-1] + s[:-1] * dx / 2
        else:
            c_up = np.concatenate(([c_in[ic]], cvec))

        # resulting concentration change
        dcdt[ic::n_comp] = -np.diff(c_up) * v / dx
        # dispersion
        dcdt[ic::n_comp] += (np.concatenate([gradc, [0]]) - np.concatenate([[0], gradc])) * D[ic] / dx

    # Reactions
    # A + B -> Product
    # unpack concentrations
    c_A = c[0::n_comp]
    c_B = c[1::n_comp]

    # dual Michaelis-Menten rate law (vectorized)
    rate = r_max * c_A / (K1 + c_A) * c_B / (K2 + c_B)

    # Rate of change of concentration (compound 1)
    dcdt[0::n_comp] -= rate
    # Rate of change of concentration (compound 2)
    dcdt[1::n_comp] -= rate
    # Rate of change of concentration (compound 3)
    dcdt[2::n_comp] += rate

    return dcdt

# =============================================================================
# PLOT FUNCTION TO VISUALIZE RESULTS
# =============================================================================
def plot_profile(t, c):
    # some of the parameter passed to plot_profile are only needed in the
    # ODE defining function ode-transport
    
    plt.figure(1)
    for ic in range(n_comp):
        plt.subplot(n_comp, 1, ic+1)
        plt.cla()
        plt.plot(x, c[ic::n_comp], 'k')
        plt.xlim([0, L])
        plt.xlabel('x [m]')
        plt.ylabel('c [mmol/l]')
        plt.title(f'{names[ic]} at t= {t:.3g} s')

    plt.draw()
    plt.pause(0.3)
    plt.show()

# =============================================================================
# Function to create a full-screen interactive window that fills the full screen
# =============================================================================
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
    fig.canvas.manager.window.setGeometry(1, dheight-1, screen_width-2, 
                                          screen_height-dheight)
    return fig


# =============================================================================
# FUNCTION TO COMPUTE THE SPARSITY PATTERN FOR TRANSPORT
# =============================================================================
def transsparse(n_comp, n_cells):
    ivec = []
    jvec = []
    avec = []
    counter = 0

    for ii in range(n_cells):
        for jj in range(n_comp):
            for kk in range(n_comp):
                ivec.append((ii) * n_comp + jj)
                jvec.append((ii) * n_comp + kk)
                avec.append(1)
                counter += 1
                # transport connection to upstream node
                if ii > 0:
                    ivec.append((ii) * n_comp + jj)
                    jvec.append((ii-1) * n_comp + kk)
                    avec.append(1)
                    counter += 1
                # transport connection to downstream node
                if ii < n_cells - 1:
                    ivec.append((ii) * n_comp + jj)
                    jvec.append((ii+1) * n_comp + kk)
                    avec.append(1)
                    counter += 1

    S = sp.coo_matrix((avec, (ivec, jvec)), 
                      shape=(n_cells*n_comp, n_cells*n_comp))
    return S

# =============================================================================
# FINALLY, HERE IS THE CALLING SCRIPT
# OneD_implicit_ADE_reactive
# =============================================================================

# Parameters
dx = 0.01          # grid spacing [m]
L = 1              # length [m]
x = np.arange(0.5*dx, L+dx, dx)  # spatial coordinates of the cell centers [m]
n_cells = len(x)   # number of cells
A = np.pi * 0.025**2  # bulk cross-sectional area [m^2]

# Flow
Q = 1e-3 / 3600    # discharge [m^3/s]
poros = 0.4        # porosity [-]
v = Q / A / poros  # seepage velocity

# Number of mobile and immobile compounds
n_mob = 3          # number of mobile compounds
n_imm = 0          # number of immobile compounds
n_comp = n_mob + n_imm  # number of compounds

names = ['A', 'B', 'Product']  # names of the compounds

# Dispersive transport parameters
alpha = 0.01      # dispersivity [m] - same for all compounds
Dp = np.array([1e-9, 0.3e-9, 0.5e-9])  # pore diffusion coefficient [m^2/s]
D = alpha*abs(v) + Dp  # dispersion coefficient of all mobile compounds [m2/s]

# TVD scheme for advection?
TVD = False

# Reactive parameters
r_max = 1e-3      # maximum reaction rate [mol/m^3/s]
K1 = 0.1          # Michaelis-Menten coefficient compound 1 [mol/m^3]
K2 = 0.1          # Michaelis-Menten coefficient compound 2 [mol/m^3]

# put all reaction parameters into a list
reacpar = (r_max,K1,K2)

# Initial concentrations
c0 = np.zeros(n_cells * n_comp)  # Initial concentrations

c_in = [1.0, 1.5, 0]  # inflow concentration [mol/m^3]

# Time span of simulation
t_start = 0                 # start time [s]
t_end   = 43200             # end time [s]
tspan   = [t_start, t_end]  # time span for ODE solver
dtout   = 600               # time increment for plotting
last_t  = t_start;

# Things needed for the ODE solver
# sparsity pattern for ODE solver
S = transsparse(n_comp, n_cells)

# Initialize graphical output
fig1 = fullscreenfigure(1)

# Set options of ODE solver
# Set up BDF solver manually with dense output enabled
solver = BDF(fun=ode_transport,
             t0=t_start,
             y0=c0,
             t_bound=t_end,
             max_step=np.inf,
             jac_sparsity=S,
             vectorized=False,
             rtol=1e-6,
             atol=1e-8)

# Store solution at output times for breakthrough curves
t_values = []
y_values = []

# Initialize plot timer
t_next_plot = t_start

# Step through the solver
while solver.status == 'running':
    solver.step()
    t_values.append(solver.t)
    y_values.append(solver.y)
    while solver.t >= t_next_plot:
       y_plot = solver.dense_output()(t_next_plot)
       plot_profile(t_next_plot, y_plot)
       t_next_plot += dtout       

# Convert recorded solution into arrays for plotting
t_values = np.array(t_values)
y_values = np.array(y_values).T  # shape: (n_vars, n_times)

# open a second window
fig2 = fullscreenfigure(2)

# plot breakthrough curve
for ic in range(n_mob):
    plt.plot(t_values,y_values[-n_comp+ic,:],label=names[ic])
plt.legend()
plt.xlabel('t [s]')
plt.ylabel('c [mmol/l]')
plt.title('Breakthrough Curves')
plt.draw()
plt.show(block=True)
