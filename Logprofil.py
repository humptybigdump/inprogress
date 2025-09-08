# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 11:09:46 2025

@author: Paula Luise Meyer
"""

# =============================================================================
# Auswertung logarithmisches Geschwindigkeitsprofil, aufgenommen an M1
# =============================================================================

# Pakete importieren
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Datei einlesen
df = pd.read_csv("H1_M1_log_Profil.csv", encoding = "utf-8")

# Variablen 
ln_v  = df["ln_v"] = np.log(df["v [m/s]"])  # logarithmierte Geschwindigkeit
ln_h = df["ln_h"] = np.log(df["h [m]"])     # logarithmierte Höhe (über Sohle)
v = df["v [m/s]"]                           # Geschwindigkeit [m/s]
h = df["h [m]"]                             # Höhe [m]

#%% Scatterplot h gegen v -> Geschwindigkeitsprofil

plt.figure(figsize = (4, 3))
plt.scatter( v, h, marker = "o")
plt.ylabel("h [m]", fontsize = 12)
plt.xlabel("$v\ [\mathrm{m\ s^{-1}}]$", fontsize = 12)
#plt.title("Geschwindigkeitsprofil M1")
plt.grid(True)
plt.tight_layout()
plt.savefig('H1_Scatter_log_Profil.png', dpi = 300)

#%% Lineare Regression

# Arrays (Wertebereich der Regressionsgerade/-kurve)
lnh_array = np.linspace(-4.7, 0, 50)
h_array = np.linspace(0.000001, 0.85, 50)

# Lineare Regression
m, b = np.polyfit(ln_h, v, 1) # erst liniearisieren (lnh) dann Regression
y_fit = m * lnh_array + b

# Parameter des logarithmischen Geschwindigkeitsprofils berechnen
kappa = 0.4
u_stern = kappa * m
z_0 = np.exp(- (kappa / u_stern) * b)

# Gefittete Geschwindigkeit berechnen

# Geschwindigkeit aus mit Regression bestimmten Paramtern berechnen
def fit(h, u_stern, kappa, z_0):
    return u_stern / kappa * np.log(h / z_0)

v_gefittet = fit(h_array, u_stern, kappa, z_0)

# Gemeinsame Abbildung linearisiertes Geschwindigkeitsprofil und nicht linearisiertes Geschwindigkeitsprofil
fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

# Plot 1: linearisiert
axes[0].scatter(v, ln_h, color="green", label="Messpunkte")
axes[0].plot(y_fit, lnh_array, color="red", label=f"v = {m:.3f}·ln(h) + {b:.3f}")
axes[0].set_ylabel(r"$\ln(z)$", fontsize=14)
axes[0].set_xlabel(r"$v\ [\mathrm{m\ s^{-1}}]$", fontsize=14)
axes[0].legend()
axes[0].grid(True)

# Plot 2: nicht linearisiert, mit gefitteter Geschwindigkeit
axes[1].scatter(v, h, color="green", label="Messpunkte")
axes[1].plot(v_gefittet, h_array, color="red",  label=fr"$v = \frac{{{u_stern:.3f}}} {{\kappa}} \cdot \ln\!\left(\frac{{z}}{{{z_0:.3f}}}\right)$")
axes[1].set_ylabel("z [m]", fontsize=14)
axes[1].set_xlabel(r"$v\ [\mathrm{m\ s^{-1}}]$", fontsize=14)
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
fig.savefig('H1_Geschwindigkeitsprofil.png', dpi = 300)

# Überprüfung der Parameter
print(f"u_stern: {u_stern}")
print(f"z_0: {z_0}")
