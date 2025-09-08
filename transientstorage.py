"""
Solve the advection-dispersion equation with transient storage via
the numerical inverse Laplace transformation using de Hoog's method

(c) Olaf A. Cirpka, February 2025
"""

# import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from invlap import invlap
matplotlib.use('QT5Agg')
from PyQt5.QtWidgets import QDesktopWidget

# Laplace transform of dual-domain transport
def c_laplace(s,x,v,D,beta,k,M,Q):
    A=Q/v
    b=s+beta*s*k/(k+s)
    alpha=(-v+np.sqrt(v**2+4*D*b))/D*0.5
    c0=M/A/np.sqrt(v**2+4*D*b)
    c=c0*np.exp(-alpha*x)
    return c

# Coefficients
x=300    # distance [m]
v=0.3    # velocity [m/s]
D=0.7    # dispersion coefficient [m2/s]
beta=.5  # ratio imobile area/mobile areas[-]
k=1e-3   # exchange coefficient [1/s]
Q=0.5    # discharge [m3/s]
M=1e-2   # mass [kg]

# time vector
tvec=np.arange(10,3610,10);
# need to pass alpha and tol to invlap when additional parameters are passed to
# the function that contains the Laplace transform
# default values are 0 and 1e-9, respectively

c  = invlap(c_laplace,tvec,0,1e-9,x,v,D,beta,k,M,Q)
c2 = invlap(c_laplace,tvec,0,1e-9,x,v,D,0,0,M,Q)

# =============================================================================
# Function that opens an interactiv window, filling the enture screen
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
    fig.canvas.manager.window.setGeometry(1, dheight-1, screen_width-2, 
                                          screen_height-dheight)
    return fig

# now plot
fig1=fullscreenfigure(1)
plt.plot(tvec,c,label='with transient storage')
plt.plot(tvec,c2,label='without transient storage')
plt.legend()
plt.xlabel('t [s]')
plt.ylabel('c [kg/m$^3$]')
plt.show(block=True)

