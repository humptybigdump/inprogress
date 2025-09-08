# -*- coding: utf-8 -*-
"""
Created on Mon May 19 17:27:43 2025

@author: lekat
"""

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

## Einlesen der Textdatei

# txt-Datei einlesen
df = pd.read_csv("tracerdaten_cor.txt", sep=";")
 
# Masse zugegebener Tracer
m = 15000 #[mg]

# Ausschließen erster Messpunkt, da t=0 und Zeit in Sekunden umrechnen
t_data = df['t_in_h'].values[1:]*3600

# Messpunktentfernung in m von der Tracerzugabestelle
x = (438.4,1763.5,3477.4,4472.3)
# Fließgeschwindigkeit in m/s aus Momentanalyse
v = (0.275,0.345,0.365,0.348)
# Abfluss in m3/s aus Momentanalyse
Q = (0.28,0.291,0.311,0.354)
# Dispersionskoeffizient in m2/s
D = (2.833,2.698,2.496,3.402)

# Vordimensionalisieren der Ergebnisse
v_opt = np.full(4, np.nan)
D_opt = np.full(4, np.nan)
Q_opt = np.full(4, np.nan)


# Definition der Modellfunktion
def modellfunktion(t, Q, D, v, x):
    return ((m * x)/(2*Q*np.sqrt(np.pi*D*t**3)))*np.exp(-((x-v*t)**2)/(4*D*t)) # Rückgabe der berechneten Konzentrationen

 
plt.figure(figsize=(12, 6))

# Farbliste definieren (z.B. Matplotlib-Standardfarben)
farben = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

# Schleife für den Parameterfit aller Messstellen
for messstelle in range(4):
    # Konzentration holen    
    c_data = df.iloc[1:, messstelle+2].values
    # Startparameter für diese Messstelle
    p0 = [Q[messstelle], D[messstelle], v[messstelle]]
    
    # Curve Fit
    params_opt, pcov = curve_fit(lambda t, Q, D, v: modellfunktion(t, Q, D, v, x[messstelle]),
                                 t_data, c_data, p0=p0)
    # Speichern
    Q_opt[messstelle], D_opt[messstelle], v_opt[messstelle] = params_opt

    # Ausgabe
    print(f"Messstelle {messstelle+1}:")
    print(f"  Q = {Q_opt[messstelle]:.4f} m³/s")
    print(f"  D = {D_opt[messstelle]:.4f} m²/s")
    print(f"  v = {v_opt[messstelle]:.4f} m/s")
    
    # Konzentration des Fits
    c_modell = modellfunktion(t_data, Q_opt[messstelle], D_opt[messstelle], v_opt[messstelle], x[messstelle])
    # Plot der Fits
    plt.plot(t_data[::12], c_data[::12], '.', color=farben[messstelle], label=f'Messdaten {messstelle+1}')
    plt.plot(t_data[::12], c_modell[::12], '-',color=farben[messstelle], label=f'ADE-Fit {messstelle+1}')


plt.xlabel('Zeit [s]', fontsize=20)
plt.ylabel('Konzentration [g/m³]', fontsize=20)
plt.grid(True)
plt.legend(fontsize=18)
plt.tick_params(axis='both', labelsize=18)

plt.tight_layout()
plt.show()



