# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:55:08 2025

@author: Pauline Fesser & Lena Oker
"""

import pandas as pd
import numpy as np

# txt-Datei mit den Tracerdaten einlesen
df = pd.read_csv("tracerdaten_cor.txt", sep=";")
# Konzentration (µg/l), M1: Spalte2, M2: Spalte3, M3: Spalte4, M4: Spalte5

# Messpunktentfernung in m von der Tracerzugabestelle
x_mess = (438.4,1763.5,3477.4,4472.3)

# Vordimensionalisieren der Ergebnisse
m0 = np.full(4, np.nan)         # Nulltes Moment
mu_tau = np.full(4, np.nan)     # Fließzeit
var_tau = np.full(4, np.nan)    # Varianz der Fließzeit
v_app = np.full(4, np.nan)      # apparente Geschwindigkeit
D_app = np.full(4, np.nan)      # apparenter Dispersionskoeffizient
Q = np.full(4, np.nan)          # Abfluss
w = np.full(4, np.nan)          # Wiederfindung

# Umrechnung der Zeit in Sekunden und extrahieren der Werte
t_h = df.iloc[:, 1].values     # Zeit (h)
t=t_h*3600                     # Zeit (s)
m = 15000                      # Tracermasse in mg 

# Schleife zur Berechnung der Parameter an allen 4 Messstellen
for messstelle in range(4):
    # Konzentration aus Dataframe holen    
    C = df.iloc[:, messstelle+2].values
    # Abstand holen
    x = x_mess[messstelle]        

    # Berechnung nulltes Moment (Fläche unter der Durchbruchskurve)
    m0[messstelle] = np.trapz(C, t) 
    # Berechnung mittlere Fließzeit in min (Erwartungswert)
    mu_tau[messstelle] = (np.trapz(C*t, t)/m0[messstelle])/60
    # Berechnung der Varianz der Fließzeit in s^2
    var_tau[messstelle]= np.trapz(C*t**2, t)/m0[messstelle] - (mu_tau[messstelle]*60)**2
    # Berechnung der apparenten Fließgeschwindigkeit
    v_app[messstelle] = x / (mu_tau[messstelle]*60)
    # Berechnung des apparenten Dispersionskoeffizienten
    D_app[messstelle] = var_tau[messstelle] * x**2 / (2 * (mu_tau[messstelle]*60)**3)
    # Berechnung des Abflusses
    Q[messstelle]= m / m0[messstelle]
    # Berechnung der Wiederfindung in % (Verdünnung)
    if messstelle < 4:
        w[messstelle] = (m0[messstelle] / m0[messstelle-1]) * 100
    # Ausgabe der berechneten Parameter
    print(f"Messstelle: {messstelle+1}")
    print(f"Mittlere Fließzeit µτ = {mu_tau[messstelle]:.3f} min")
    print(f"Varianz der Fließzeit σ²τ = {var_tau[messstelle]:.3f} s²")
    print(f"Apparente Geschwindigkeit v_app = {v_app[messstelle]:.3f} m/s")
    print(f"Apparenter Dispersionskoeffizient D_app = {D_app[messstelle]:.6e} m²/s")
    print(f"Nulltes Moment m0 = {m0[messstelle]:.3f}")
    print(f"Apparenter Durchfluss Q = {Q[messstelle]:.3f} m³/s")
    print(f"Wiederfindungsrate w = {w[messstelle]:.3f} %")
    
# Dataframe mit Parametern erstellen und als csv_Datei speichern
df_parameter = pd.DataFrame(
    [m0, mu_tau, var_tau, v_app, D_app, Q, w],
    index=["m0", "mu_tau [min]", "var_tau [s^2]", "v_app [m/s]", "D_app [m^2/s]", "Q [m^3/s]", "Wiederfindung[%]"],
    columns=[f"Messstelle {i+1}" for i in range(4)]
)

print(df_parameter)
#df_parameter.round(3).to_csv("momentanalyse_parameter_4.csv", sep=";") # bei Bedarf auskommentieren 
    
    
    
    
    