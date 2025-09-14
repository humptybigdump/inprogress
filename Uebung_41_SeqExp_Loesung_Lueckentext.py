"""
Uebung 4.1: Implementierung einer seq-expliziten, partitionierten Kopplungsstrategie

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-07

Fragen & Aufgaben:
1. Ergänzen Sie die fehlenden Stellen so, dass eine serielle explizite
   Kopplung zwischen CFD & CSD entsteht.
2. Wählen Sie eine dt=1e-3s. Warum lässt sich keine Lösung erzielen?
3. Bestimmen Sie das kritische Dichteverhältnis bevor es bei dt=1e-3s zur Instabilität kommt?
4. Was passiert wenn Sie für die Dichte aus 3 verschiedene Zeitschrittweiten
   verwenden (1e-2, 2e-3, 9e-4, 5e-4, 1e-4, 1e-5, 1e-6)? Für den späteren Vergleich
   bitte alle Bilder mit Zeitschrittweite abspeichern!
5. Woher kommt die verbliebene Abweichung zwischen zur analytischen Lösung?
6. Wählen Sie eine Wasserdichte von 1 kg/m3 (Uebung_30_Loesung und Variablen!).
   Welcher Einfluss hat die Zeitschrittweite auf die Abweichung zur Referenzlösung
   (5e-4, 1e-4, 5e-5)?
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

x        = np.zeros([gv.N+1])     # [m]
dx       = ?     # [m/s]
ddx      = ?     # [m/s2]
t        = ?     # [s]

for n in np.arange(gv.N-1):
    pw_old                    = copy.deepcopy(pw)
    x[n+1], dx[n+1], ddx[n+1] = ?    
    pw                        = ?    
    t[n+1]                    = gv.dt + t[n]    
    x_res                     = ((((x[n+1] - x[n+1])/x[n+1])**2)**0.5)
    p_res                     = ((((pw_old - pw)/pw)**2)**0.5)
    x_diff                    = ((((x[n+1] - x[n])/x[n+1])**2)**0.5)
    print(n, x_res, p_res, x_diff)

# Jetzt wird die analytische Referenzlösung bestimmt    
xEnde, x_a, dx_a, ddx_a, t_a  = ana.calcAnalytical()
    
plotte.plotDiagrams(f'SeqExp_rhoW{(gv.rhoW)}_dt{str(gv.dt)}',t_a,x_a,dx_a,ddx_a,t,x,dx,ddx)