"""
Uebung 4.2: Implementierung einer impliziten, partitionierten Kopplungsstrategie

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-07

Aufgaben:
1. Erweitern Sie das Programm auf eine implizite Kopplungsstrategie.
   Die analytische Lösung soll mit einer Zeitschrittweite von 5e-6
   gerechnet werden. Dichte von Wasser ist in beiden Fällen 420 kg/m3
2. Prüfen Sie den Stabilitätsbereich des Algorithmus in Abhängigkeit
   der Zeitschrittweite (1e-2, 1e-3, 1e-5, 5e-6).
   Was beobachten Sie in den Subiterationen?
3. Erklären Sie das Ergebnis.
"""

# Import der benötigten Module
import Uebung_30_Loesung as ana
import Uebung_30_Variablen as gv
import Uebung_31_Loesung as csd
import Uebung_32_Loesung as cfd
import Uebung_30_Diagramme as plotte
import numpy as np
import copy

x_res    = 1000                   # Startwert: Differenz zwischen den Positionen des Interfaces zum gleichen Zeitpunkt
p_res    = 1000                   # Startwert: Differenz zwischen den Drücken am Interface, die berechnet und verwendet wurden
x_dif    = 1000                   # Startwert: Differenz der Positionen zweier aufeinanderfolgenden Zeitpunkten
pw       = 800000                 # Startwert: Druck zum Zeitpunkt 0

x        = np.zeros([gv.N+1])     # [m]
dx       = np.zeros([gv.N+1])     # [m/s]
ddx      = np.zeros([gv.N+1])     # [m/s2]
t        = np.zeros([gv.N+1])     # [s]

# Zusätzliche Variablen für die implizite Kopplung / t entspricht temporär.
subiter   = 5                                # Maximale Anzahl an Subiterationen
xt        = np.zeros([(gv.N+1)*subiter])     # [m]     Positionen während der Subiterationen
dxt       = np.zeros([(gv.N+1)*subiter])     # [m/s]   Geschwindigkeiten während der Subiterationen
ddxt      = np.zeros([(gv.N+1)*subiter])     # [m/s2]  Beschleunigungen während der Subiterationen
tt        = np.zeros([(gv.N+1)*subiter])     # [s]     Pseudo-Zeit für die Ausgabe

for n in np.arange(gv.N-1):    

   # Zu Beginn einer impliziten Sub-Schleife werden die Werte initialisiert
   xt[n*subiter]   = x[n]      
   dxt[n*subiter]  = dx[n]
   ddxt[n*subiter] = ddx[n]

   for k in np.arange(subiter):
        pw_old                                                    = copy.deepcopy(pw)                        # Wird gespeichert um zu überprüfen, ob die dyn. Kopplungsbedingung im Gleichgewicht ist
        xt[n*subiter+k+1], dxt[n*subiter+k+1],ddxt[n*subiter+k+1] = ?
        pw                                                        = ?
        x[n+1]                                                    = ?
        dx[n+1]                                                   = ?
        ddx[n+1]                                                  = ?
        tt[n*subiter+k+1]                                         = gv.dt/subiter + tt[n*subiter+k]
        print(k,pw_old, pw,xt[n*subiter+k+1])
        
   t[n+1]                    = gv.dt + t[n]    
   x_res                     = ((((x[n+1] - x[n+1])/x[n+1])**2)**0.5)
   p_res                     = (((pw_old - pw)/pw)**2)**0.5
   x_diff                    = ((((x[n+1] - x[n])/x[n+1])**2)**0.5)
   print(n, x_res, p_res, x_diff)


# Jetzt wird die analytisch Referenzlösung bestimmt    
xEnde, x_a, dx_a, ddx_a, t_a  = ana.calcAnalytical()
    
plotte.plotDiagrams(f'Imp_rhoW{(gv.rhoW)}_dt{str(gv.dt)}',t_a,x_a,dx_a,ddx_a,tt,xt,dxt,ddxt)