# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:22:30 2025

@author: Olaf Cirpka

verändert von: Pauline Fesser und Lena Oker 

Hinweis: Datei deconvolution.py wird benötigt
"""
import numpy as np
import pandas as pd
import scipy.linalg as la
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from deconvolution import deconvolution
from datetime import timedelta
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
# Einlesen der Daten 
# txt-Datei einlesen
df = pd.read_csv("tracerdaten_cor.txt", sep=";")

# Zeit 
t=df['t_in_h']*3600 # Zeit seit Zugabe in Sekunden 
dt = 5              # Zeitabstand zwischen den Messpunkten win Sekunden

# coefficients for the deconvolution
sigma = 0.1            # initial guess for standard deviation of EC 
n_g = 1800             # length of the transfer function
theta = 3.85e-13       # slope of the variogram [s^-3]
choice = 'smooth'      # choice of estimation, alternativ: condreal
submean = False        # subtract the mean values?
firstzero = True       # first value to be zero?
zerobefore = True      # are the in- and output signals zero before the measurements?
nreal = 100            # number of realizations

# Schleife für jede Messstelle
for MS in range(3):
    cin=df.iloc[:, MS+2].values  # Inputsignal (oberstromige Messstelle)
    cout=df.iloc[:, MS+3].values # Outputsignal (unterstromige Messstelle)

    # run the deconvolution code                    # Aufruf der Funktion deconvolution aus deconvolution.py und Berechnung der Transferfunktion
    g_est, std_g, y_sim, std_y, theta, sigma = \
    deconvolution(cin, cout, dt, theta, sigma, n_g,
                  choice, submean, firstzero, zerobefore, nreal) # g_est ist die geschätzte Transferfunktion, std_g die Standardabweichung der Transferfunktion 

    match choice:
        case 'smooth':                              # für smooth (nur eine geglättete Transferfunktion)
            y_mean = y_sim[:,0]                     # simulierte Kurve
            g_l = g_est - std_g                     # untere Grenze Konfidenzbereich       
            g_h = g_est + std_g                     # obere Grenze Konfidenzbereich
            g_mean = g_est
        case _:                                     # für alle anderen Varianten z.B. condreal (verschiedene Realisierungen der Transferfunktion)
            y_mean=np.mean(y_sim,axis=1)            # mittleres simuliertes Outputsignal 
            g_l = np.quantile(g_est,0.1587,axis=1)  # Berechnung Unsicherheitsbereich (15%-84%) 
            g_h = np.quantile(g_est,0.8413,axis=1)
            g_mean=np.mean(g_est,axis=1)            # Mittelwert über alle Realisierungen der Transferfunktion 
    # Berechnung Momente der Transferfunktion
    m0=sum(g_mean)*dt                               # 0.Moment (Wiederfindung)
    tvec_g=np.arange(n_g)*dt                        # Zeitvektor in Sekunden, der zu den Indizes der Transferfunktion passt
    m1=sum(tvec_g*g_mean)*dt                        # 1.Moment
    mean_tau = m1/m0                                # mittlere Fließzeit
    m2c=sum((tvec_g-mean_tau)**2 *g_mean)*dt        # zweites Zentralmoment
    var_tau = m2c/m0                                # Varianz der Fließzeit
    
    # Ausgabe der Parameter
    print(f'Abschnitt {MS+1} -> {MS+2}')
    print(f'recovery:             {m0:5.3f}')
    print(f'mean travel time:   {mean_tau:5.0f} s')
    print(f'std of travel time: {np.sqrt(var_tau):5.0f} s')

    fig = fullscreenfigure(MS+1)

    # Subplot 1 (Messdaten und Simulation)
    ax1 = plt.subplot(2,1,1)
    plt.plot(t,cout,'k-',label=f'M{MS+2} gemessen') # Messdaten Outputsignal
    plt.plot(t,y_mean,'r-',label='simuliert')       # Simulation Outputsignal
    plt.xlabel('Zeit [s]', fontsize=25)
    plt.ylabel('c [\u03BCg/l]', fontsize=25)
    plt.legend(fontsize=34)
    plt.tick_params(axis='both', labelsize=25)
    plt.grid(True)
    
    # Subplot 2 (Transferfunktion)
    ax2=plt.subplot(2,1,2)
    plt.plot(np.arange(n_g)*dt,g_mean,'k',label='mean')
    ax2.fill_between(np.arange(n_g)*dt, g_l, g_h,  color='k', 
                alpha=0.25, edgecolor=None, 
                label='16%-84%')
    plt.xlabel('\u03C4 [s]', fontsize=25)
    plt.ylabel('g(\u03C4) [1/s]', fontsize=25)
    plt.legend(fontsize=30)
    plt.title(f'Transfer Function M{MS+1} → M{MS+2}', fontsize=25)
    plt.tick_params(axis='both', labelsize=25)
    plt.grid(True)
    fig.canvas.draw_idle()
    plt.show(block=False)
    plt.pause(0.1)

plt.show(block=True)

