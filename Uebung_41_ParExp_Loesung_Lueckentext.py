"""
Uebung 4.1: Implementierung einer parallel-expliziten, partitionierten Kopplungsstrategie

Autor: Mark-Patrick Mühlhausen

Datum: 2024-07-29

Fragen:
0. Ergänzen Sie die fehlenden Stellen, sodass ein paralleler expliziter
   Algorithmus entsteht.
1. Verwenden Sie dasselbe kritische Dichteverhältnis wie beim sequentiellen
   Algorithmus (auch in der analytischen Lösung). Welchen Einfluss hat die
   Zeitschrittweite diesmal (1e-2,1e-3,1e-5,1e-6)?
2. Welchen Einfluss hat die Zeitschrittweite auf die Abweichung zur Referenzlösung?
3. Vergleichen Sie die Lösungen des seriellen & des parallelen Algorithmus
   bei dt=8e-4s (rhoW = 420 kg/m3). Was fällt auf?
"""

# Import der benötigten Module
import Uebung_30_Loesung as ana
import Uebung_30_Variablen as gv
import Uebung_31_Loesung as csd
import Uebung_32_Loesung as cfd
import Uebung_30_Diagramme as plotte
import numpy as np
import copy

x_res    = 1000                   # Startwert
p_res    = 1000                   # Startwert
x_dif    = 1000                   # Startwert
pw       = 0                      # Startwert

x        = ?     # [m]
dx       = ?     # [m/s]
ddx      = ?     # [m/s2]
t        = ?     # [s]

for n in np.arange(gv.N-1):
    pw_old                    = copy.deepcopy(pw)
    x[n+1], dx[n+1], ddx[n+1] = ?    
    pw                        = ?    
    t[n+1]                    = ?    
    x_res                     = ((((x[n+1] - x[n])/x[n+1])**2)**0.5)
    p_res                     = ((((pw_old - pw)/pw)**2)**0.5)
    x_diff                    = ((((x[n+1] - x[n])/x[n+1])**2)**0.5)
    print(n, x_res, p_res, x_diff)

# Jetzt wird die analytisch Referenzlösung bestimmt    
xEnde, x_a, dx_a, ddx_a, t_a  = ana.calcAnalytical()
    
plotte.plotDiagrams(f'ParExp_rhoW{(gv.rhoW)}_dt{str(gv.dt)}',t_a,x_a,dx_a,ddx_a,t,x,dx,ddx)