# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 14:04:11 2025

@author: Paula Luise Meyer
"""
# Pakete
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# Abbildung Querschnitt und Fließgeschwindigkeiten (Für M2a)
# =============================================================================

# Daten des Tauchstabs nach Jens
dfJ1 = pd.read_csv("S2J_11.csv", encoding="utf-8")
dfJ2 = pd.read_csv("S2J_12.csv", encoding="utf-8")
dfJ3 = pd.read_csv("S2J_13.csv", encoding="utf-8")

# Variablen erstellen (Geschwindigkeiten gemessen mit Tauchstab)
vJ1 = dfJ1['v [m/s]']
vJ2 = dfJ2['v [m/s]']
vJ3 = dfJ3['v [m/s]']

# Daten des OTT MF Pro
dfO1 = pd.read_csv("FPS2_0808.csv", encoding="utf-8", sep = '\t', decimal = ',')
dfO2 = pd.read_csv("FPS2_0808_2.csv", encoding="utf-8", sep = '\t', decimal = ',')
dfO3 = pd.read_csv("FPS2_0808_3.csv", encoding="utf-8", sep = '\t', decimal = ',')

# Variablen erstellen (Geschwindigkeiten gemessen mit OTT MF Pro)
vO1 = dfO1['mittlere Geschw. (m/s)']
vO2 = dfO2['mittlere Geschw. (m/s)']
vO3 = dfO3['mittlere Geschw. (m/s)']

# Lotrechte in Lage umrechnen
Lage= dfO1['Lage (m)'] - 0.2 # das Ufer ist bei 0.2 m auf dem Maßband

# Leeres DataFrame für die Durchschnittsgeschwindigkeiten pro Messlotrechte: Tauchstab: 'meanJ_LR'
meanJ_LR = pd.DataFrame(columns=['meanJ_LR'])

# Mit for-Schleife füllen
for i in range(0, 17):
    mean_value = (vJ1[i] + vJ2[i] + vJ3[i])/3
    meanJ_LR.loc[i] = mean_value  # Zeile hinzufügen

# Ausgabe mittlere Geschwindigkeiten Tauchstab
print(meanJ_LR)
print('\n')

# Leeres DataFrame für die Durchschnittsgeschwindigkeiten pro Messlotrechte: OTT MF Pro: 'meanO_LR'
meanO_LR = pd.DataFrame(columns=['meanO_LR'])

# Mit for-Schleife füllen
for i in range(0, 17):
    mean_value = (vO1[i] + vO2[i] + vO3[i])/3
    meanO_LR.loc[i] = mean_value  # Zeile hinzufügen

# Ausgabe mittlere Geschwindigkeiten OTT MF Pro
print(meanO_LR)

# Plot erstellen
fig, ax1 = plt.subplots(figsize=(7, 3))

ax1.scatter(Lage, meanO_LR, color="tab:blue", marker="x", s = 70, label="OTT MF Pro")
ax1.scatter(Lage, meanJ_LR, color="tab:red", marker="*", s= 70, label="Tauchstab")

ax1.set_ylabel("Geschwindigkeit v [m s$^{-1}$]", fontsize = 13)
ax1.set_xlabel("Abstand linkes Ufer [m]", fontsize = 13)
ax1.tick_params(axis="y")
#ax1.set_title("Abfluss und Geschwindigkeit während des Tracerversuchs")
ax1.grid(True)
ax1.legend()
plt.tight_layout()
plt.savefig('H1_Lotrechten.png', dpi=300)