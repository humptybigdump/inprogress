"""
Uebung 3.1

Das Antwortverhalten des Stopfens wird in einer Funktion modelliert, sodass
sie später vom Kopplungsprogramm aufgerufen werden kann.

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-07
"""

import Uebung_30_Variablen as gv
import copy

def calcStopfen(pw, x, dx, ddx):
    dx_old = ?
    ddx    = ?
    dx     = ddx*? + dx
    x      = (dx + dx_old)/2*gv.dt + x
        
    return x, dx, ddx
