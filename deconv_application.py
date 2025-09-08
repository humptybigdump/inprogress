# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:22:30 2025

@author: Olaf
"""
import numpy as np
import pandas as pd
import scipy.linalg as la
import matplotlib.pyplot as plt
import matplotlib
from deconvolution import deconvolution
matplotlib.use('QT5Agg')
from PyQt5.QtWidgets import QDesktopWidget


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

# =============================================================================
# Main script
# =============================================================================
# Read all data of River Thur
data = pd.read_csv('Thur.csv', sep=';')
names = data.columns.tolist()
date = pd.to_datetime(data.Date,dayfirst=True) # convert Date into datetime
dt   = date[1] - date[0]                 # dt in Timedelta
dt   = dt.total_seconds()/86400          # dt in days
nt   = len(data.Date)                    # number of time points

# detrending of the data (dt must be in days)
def detrend(signal,dt,n):
    # removes a constant mean, as well as 
    # sines and cosines with periods of 1/year to n/year
    nt=len(signal)
    X=np.ones((nt,2*n+1))
    t=np.array(range(nt))*dt
    for i in range(n):
        X[:,i*2+1]=np.sin(2*np.pi*t/365*(i+1))
        X[:,i*2+2]=np.cos(2*np.pi*t/365*(i+1))
    filtered = signal-X@la.solve(X.T@X,X.T@signal)
    return filtered

# all EC series detrended
Sigdetrend = detrend(data.iloc[:,1:].to_numpy(),dt,4)
# input signal is the river EC time series
Sigin  = Sigdetrend[:,0]
namein=names[1]
# potential output signal are all other EC time series
Sigout = Sigdetrend[:,1:]
namesout=names[2:]

# coefficients for the deconvolution
sigma = 15             # initial guess for standard deviation of EC
n_g = 150              # length of the transfer function
theta = 0.1            # slope of the variogram [d^-3]
choice = 'est_theta'   # choice of estimation
submean = True         # subtract the mean values?
firstzero = True       # first value to be zero?
nreal = 100            # number of realizations
select = 1             # selection of output signal
# run the deconvolution code
g_est, std_g, y_sim, std_y, theta, sigma = \
    deconvolution(Sigin,Sigout[:,select],dt,theta,sigma,n_g,
                  choice,submean,firstzero,nreal)

# plots
# plot the original EC time series
fig1 = fullscreenfigure(1)
plt.plot(date,data.iloc[:,1:],label=names[1:])
plt.legend()
plt.xlabel('date')
plt.ylabel('EC [\u03BCS/cm]')
plt.title('Original EC Time Series')

# plot the detrended EC time series
fig2 = fullscreenfigure(2)
plt.plot(date,Sigin,label=namein)
plt.plot(date,Sigout,label=namesout)
plt.legend()
plt.xlabel('date')
plt.ylabel('EC detrended [\u03BCS/cm]')
plt.title('Detrended EC Time Series')
    
match choice:
    case 'smooth':
       y_mean = y_sim[:,0]
       g_l = g_est - std_g
       g_h = g_est + std_g
       g_mean = g_est
    case _:
       y_mean=np.mean(y_sim,axis=1)
       g_l = np.quantile(g_est,0.1587,axis=1)
       g_h = np.quantile(g_est,0.8413,axis=1)
       g_mean=np.mean(g_est,axis=1)       

fig3=fullscreenfigure(3)
ax = plt.subplot(2,1,1)
plt.plot(date,Sigout[:,1],'k-',label='measured')
plt.plot(date[n_g-1:],y_mean,'r-',label='simulated')
plt.xlabel('date')
plt.ylabel('EC detrended [\u03BCS/cm]')
plt.legend()
plt.title(f'EC Times Series of {namesout[select]}')

ax=plt.subplot(2,1,2)
plt.plot(np.arange(n_g)*dt,g_mean,'k',label='mean')
ax.fill_between(np.arange(n_g)*dt, g_l, g_h,  color='k', 
                alpha=0.25, edgecolor=None, 
                label='16%-84%')
plt.xlabel('\u03C4 [d]')
plt.ylabel('g(\u03C4) [1/d]')
plt.legend()
plt.title(f'Transfer Function {namein} \u2192 {namesout[select]}')

plt.show(block=True)
