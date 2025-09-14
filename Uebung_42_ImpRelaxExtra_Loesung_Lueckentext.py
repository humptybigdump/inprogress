"""
Uebung 4.2: Implementierung einer impliziten, partitionierten Kopplungsstrategie
--> ZEIT IST GELD :-) Beschleunigen Sie die Rechnung durch Extrapolation

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-08

Aufgaben: Ausgangspunkt ist subiter=20, dt=5e-5, alpha=0.3
1. Ergänzen sie die ? analog zur letzten Übung. Bestimmen Sie die Gesamtlaufzeit des Programmes mit dem Modul timeit.

2. Programmieren Sie ein Abbruchkriterium für die impliziten Iterationen. Abbruch, wenn p_res < 1e-9. Lassen Sie sich k ausgeben. Messen Sie die Zeit. Wie kann p_res gewählt werden, dass Ergebnis optisch gut übereinstimmt
3. Optimieren Sie die Laufzeit, durch Extrapolation von x, dx innerhalb der impliziten Schleife
4. Optimieren Sie die Laufzeit durch die Anpassung des Relaxationsparameters für pw.
5. Wie kann man es noch weiter beschleunigen?
"""

# Import der benötigten Module
import Uebung_30_Loesung as ana
import Uebung_30_Variablen as gv
import Uebung_31_Loesung as csd
import Uebung_32_Loesung as cfd
import Uebung_30_Diagramme as plotte
import numpy as np
import copy
import timeit

start = timeit.default_timer()

x_res    = 1000                   # Startwert: Differenz zwischen den Positionen des Interfaces zum gleichen Zeitpunkt
p_res    = 1                      # Startwert: Differenz zwischen den Drücken am Interface, die berechnet und verwendet wurden
x_dif    = 1000                   # Startwert: Differenz der Positionen zweier aufeinanderfolgenden Zeitpunkten
pw       = 800000                 # Startwert: Druck zum Zeitpunkt 0

x        = np.zeros([gv.N+1])     # [m]
dx       = np.zeros([gv.N+1])     # [m/s]
ddx      = np.zeros([gv.N+1])     # [m/s2]
t        = np.zeros([gv.N+1])     # [s]

# Zusätzliche Variablen für die implizite Kopplung / t entspricht temporär.
subiter   = 20                               # Maximale Anzahl an Subiterationen
xt        = np.zeros([(gv.N+1)*subiter])     # [m]     Positionen während der Subiterationen
dxt       = np.zeros([(gv.N+1)*subiter])     # [m/s]   Geschwindigkeiten während der Subiterationen
ddxt      = np.zeros([(gv.N+1)*subiter])     # [m/s2]  Beschleunigungen während der Subiterationen
tt        = np.zeros([(gv.N+1)*subiter])     # [s]     Pseudo-Zeit für die Ausgabe
alpha     = 0.3                             # [-]     Relaxationsfaktor

for n in np.arange(gv.N-1):    

   # Zu Beginn einer impliziten Sub-Schleife werden die Werte initialisiert
   xt[n*subiter]   = x[n] + gv.dt*dx[n]      
   dxt[n*subiter]  = dx[n] + gv.dt*ddx[n]
   ddxt[n*subiter] = ddx[n]

   for k in np.arange(subiter):
        pw_old                                                    = copy.deepcopy(pw) # Wird gespeichert um zu überprüfen, ob die dyn. Kopplungsbedingung im Gleichgewicht ist
        xt[n*subiter+k+1], dxt[n*subiter+k+1],ddxt[n*subiter+k+1] = ?
        ?
        dxt[n*subiter+k+1]                                        = ?
        pw                                                        = ?
        ?
        tt[n*subiter+k+1]                                         = gv.dt/subiter + tt[n*subiter+k]
        p_res                                                     = (((pw_old - pw)/pw)**2)**0.5
        
        ?
            x[n+1]                                                    = xt[n*subiter+k+1]
            dx[n+1]                                                   = dxt[n*subiter+k+1]
            ddx[n+1]                                                  = ddxt[n*subiter+k+1]
            break
        print k,pw_old, pw,xt[n*subiter+k+1]
        
   t[n+1]                    = gv.dt + t[n]    
   x_res                     = ((((x[n+1] - x[n+1])/x[n+1])**2)**0.5)
   #p_res                     = (((pw_old - pw)/pw)**2)**0.5
   x_diff                    = ((((x[n+1] - x[n])/x[n+1])**2)**0.5)
   print(n, k, x_res, p_res, x_diff)


# Jetzt wird die analytisch Referenzlösung bestimmt    
xEnde, x_a, dx_a, ddx_a, t_a  = ana.calcAnalytical()
    
plotte.plotDiagrams(f'ImpRelaxExtraRes_rhoW{(gv.rhoW)}_dt{str(gv.dt)}_subiter{str(subiter)}_alpha{str(alpha)}',t_a,x_a,dx_a,ddx_a,t,x,dx,ddx)

end = timeit.default_timer()

print(end - start)