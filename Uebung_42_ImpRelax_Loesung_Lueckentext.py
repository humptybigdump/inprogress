"""
Uebung 4.2: Implementierung einer impliziten, partitionierten Kopplungsstrategie
            mit Relaxation zur Verbesserung der Stabilität
            
Autor: Mark-Patrick Mühlhausen

Datum: 2024-08-07

Aufgaben:
0. Erweitern Sie das Programm um eine Positions- und eine Last-Relaxation. [25 Min]
1. Berechnen Sie die Lösung für (alpha = 0.5, rhoW = 420, subiter = 5). Bestimmen
   Sie den Stabilitaetsbereich in Abhaengigkeit der Zeitschrittweiten (1e-2, 1e-3, 1e-4, 1e-5, 5e-6) [20 Min]
2. Vergleichen Sie die beiden Setups (dt=5e-4, subiter=3 und subiter=8):
   Schauen Sie sich die inneren Iterationen und das Ergebnis an [10 Min]
3. Was passiert wenn Sie einen alpha-Wert von 0.05 wählen bei Subiter 8 und dt5e-4? [15 Min]
4. Fassen Sie ihre Erkenntnisse über den Relaxationsfaktor zusammen. [15 Min]
5. Erhöhen Sie nun die Dichte rhoW auf 1000kg/m3 um das korrekte Problem zu betrachten (dt=1e-5s). 
   Bestimmen Sie alpha und subiter so, dass eine gute Übereinstimmung mit der Lösung eintritt. [15 Min]
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
subiter   = 5                               # Maximale Anzahl an Subiterationen
xt        = np.zeros([(gv.N+1)*subiter])     # [m]     Positionen während der Subiterationen
dxt       = np.zeros([(gv.N+1)*subiter])     # [m/s]   Geschwindigkeiten während der Subiterationen
ddxt      = np.zeros([(gv.N+1)*subiter])     # [m/s2]  Beschleunigungen während der Subiterationen
tt        = np.zeros([(gv.N+1)*subiter])     # [s]     Pseudo-Zeit für die Ausgabe
alpha     = 0.5                              # [-]     Relaxationsfaktor

for n in np.arange(gv.N-1):    

   # Zu Beginn einer impliziten Sub-Schleife werden die Werte initialisiert
   xt[n*subiter]   = x[n]      
   dxt[n*subiter]  = dx[n]
   ddxt[n*subiter] = ddx[n]

   for k in np.arange(subiter):
        pw_old                                                    = copy.deepcopy(pw)                        # Wird gespeichert um zu überprüfen, ob die dyn. Kopplungsbedingung im Gleichgewicht ist
        xt[n*subiter+k+1], dxt[n*subiter+k+1],ddxt[n*subiter+k+1] = ?
        ?
        pw                                                        = ?
        ?
        x[n+1]                                                    = ?
        dx[n+1]                                                   = ?
        ddx[n+1]                                                  = ?
        tt[n*subiter+k+1]                                         = gv.dt/subiter + tt[n*subiter+k]
        print(k,pw_old, pw,xt[n*subiter+k+1])
        
   t[n+1]                    = gv.dt + t[n]    
   x_res                     = ((((x[n+1] - x[n+1])/x[n+1])**2)**0.5)
   p_res                     = (((pw_old - pw)/pw)**2)**0.5
   x_diff                    = ((((x[n+1] - x[n])/x[n+1])**2)**0.5)
   if (n%1 == 0):
       print(n, x_res, p_res, x_diff)


# Jetzt wird die analytisch Referenzlösung bestimmt    
xEnde, x_a, dx_a, ddx_a, t_a  = ana.calcAnalytical()
    
plotte.plotDiagrams(f'IR_rhoW{(gv.rhoW)}_dt{str(gv.dt)}_subit{str(subiter)}_alp{str(alpha)}',t_a,x_a,dx_a,ddx_a,tt,xt,dxt,ddxt)