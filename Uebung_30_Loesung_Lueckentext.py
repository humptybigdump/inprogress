"""
Uebung 3.0

Lösung der Bestimmungsgleichung fuer das gekoppelte Problem Stopfen und Rohr

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-06
"""

import numpy as np
import Uebung_30_Variablen_Lueckentext as gv

def calcAnalytical():

    # Numerik
    dt          = ?                # [s] Zeitschrittweite
    N           = 1/dt                # [-] Anzahl Zeitschritte
    
    # Variablen zu Beginn: Der Stopfen ist in Ruhe
    x           = np.zeros([N+1])     # [m]
    dx          = ?     # [m/s]
    ddx         = ?     # [m/s2]
    t           = ?     # [s]
    
    for n in np.arange(N):
        #print n
        ddx[n+1] = ?
        dx[n+1]  = (ddx[n] + ddx[n+1])/2*dt + dx[n]
        x[n+1]   = (dx[n+1]+dx[n])/2*dt + x[n]
        t[n+1]   = dt + t[n]
    
    # Stationaere Endlage
    xEnde     = ?
    
    return xEnde, x, dx, ddx, t