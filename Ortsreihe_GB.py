# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 12:14:09 2025

@author: Paula Luise Meyer
"""
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# Ortsreihe des Durchflusses zur Zeit des Tracerversuchs
# =============================================================================

# Dateien einlesen (Durchflusszeitreihen)
dfM1 = pd.read_csv("M1_Durchflusszeitreihe.csv", encoding="utf-8")
dfM2 = pd.read_csv("M2_Durchflusszeitreihe.csv", encoding="utf-8")
dfM3 = pd.read_csv("M3_Durchflusszeitreihe.csv", encoding="utf-8")
dfM4 = pd.read_csv("M4_Durchflusszeitreihe.csv", encoding="utf-8")
dfMGB = pd.read_csv("MGB_Durchflusszeitreihe.csv", encoding="utf-8")

# Fließgeschwindigkeiten zur Zeit des Tracerversuchs [m/s] (berechnet in Durchfluss_und_Druecke.xlsx)
v1_mean = 0.15
v2_mean = 0.36
v3_mean = 0.24
v4_mean = 0.19

# datetime als Index
dfM1["datetime"] = pd.to_datetime(dfM1["datetime"], format="%Y-%m-%d %H:%M:%S")
dfM1.set_index("datetime", inplace = True)
dfM2["datetime"] =pd.to_datetime(dfM2["datetime"], format="%Y-%m-%d %H:%M:%S")
dfM2.set_index("datetime", inplace = True)
dfM3["datetime"] = pd.to_datetime(dfM3["datetime"], format="%Y-%m-%d %H:%M:%S")
dfM3.set_index("datetime", inplace = True)
dfM4["datetime"] = pd.to_datetime(dfM4["datetime"], format="%Y-%m-%d %H:%M:%S")
dfM4.set_index("datetime", inplace = True)
dfMGB["datetime"] = pd.to_datetime(dfMGB["datetime"], format="%Y-%m-%d %H:%M:%S")
dfMGB.set_index("datetime", inplace = True)

# Variablen der Durchflüsse erstellen
Q1 = dfM1['Q_curve [m^3/s]']
Q2 = dfM2['Q_curve [m^3/s]']
Q3 = dfM3['Q_curve [m^3/s]']
Q4 = dfM4['Q_curve [m^3/s]']
QGB = dfMGB['Q_curve [m^3/s]']

# Start- und Endzeit des Tracerversuchs
start = pd.to_datetime("2025-08-10 21:50:25")
end   = pd.to_datetime("2025-08-11 02:50:25")

# Daten im Zeitfenster auswählen
mask1 = (dfM1.index >= start) & (dfM1.index<= end)
mask2 = (dfM2.index >= start) & (dfM2.index <= end)
mask3 = (dfM3.index >= start) & (dfM3.index <= end)
mask4 = (dfM4.index >= start) & (dfM4.index <= end)
maskGB = (dfMGB.index >= start) & (dfMGB.index <= end)

# Mittelwerte berechnen und ausgeben
Q1_mean = Q1[mask1].dropna().mean()
Q2_mean = Q2[mask2].dropna().mean()
Q3_mean = Q3[mask3].mean()
Q4_mean = Q4[mask4].mean()
QGB_mean = QGB[maskGB].mean()

print("Mittelwert Q1 [m^3/s]:", Q1_mean)
print("Mittelwert Q2 [m^3/s]:", Q2_mean)
print("Mittelwert Q3 [m^3/s]:", Q3_mean)
print("Mittelwert Q4 [m^3/s]:", Q4_mean)
print("Mittelwert QGB [m^3/s]:", QGB_mean)

# Mittlerer Anteil Goldersbach zur Zeit des Tracerversuchs
AnteilGB_mean = QGB_mean/Q4_mean*100
print(f'Mittlerer Anteil GB zur Zeit des Tracerversuchs: {AnteilGB_mean} %')

# Liste der Mittelwerte erstellen
Qmeans = [Q1_mean, Q2_mean, Q3_mean, Q4_mean]
vmeans = [v1_mean, v2_mean, v3_mean, v4_mean,]
labels = ["M1", "M2", "M3", "M4"]

# Plot erstellen
fig, ax1 = plt.subplots(figsize=(4, 3))

# Erste Achse: Abfluss
ax1.scatter(labels, Qmeans, color="tab:blue", marker="o", label="Abfluss")
ax1.set_ylabel("Abfluss [m$^3$ s$^{-1}$]", color="tab:blue")
ax1.set_xlabel("Messstelle")
ax1.tick_params(axis="y", labelcolor="tab:blue")
#ax1.set_title("Abfluss und Geschwindigkeit während des Tracerversuchs")
ax1.grid(True)

# Zweite Achse: Geschwindigkeit
ax2 = ax1.twinx()
ax2.scatter (labels, vmeans, color="tab:red", label="Geschwindigkeit")
ax2.set_ylabel("Geschwindigkeit [m s$^-1$]", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

fig.tight_layout()
fig.savefig('H1_Ortsreihe.png', dpi=300)
plt.show()

#%% ===========================================================================
# Anteil/Einfluss des Goldersbachs darstellen
# =============================================================================

Q3GB = Q3 + QGB                     # Summe Q3 und Goldersbach
Q3GB_clean = Q3GB.dropna()          # nan-Werte entfernen
AnteilGB = QGB/Q4*100               # in %
AnteilGB_clean = AnteilGB.dropna() 
differenzQ3GBQ4 = Q3GB - Q4
differenzQ3GBQ4_clean = differenzQ3GBQ4.dropna()

# Plot erstellen
fig, ax1 = plt.subplots(figsize=(6, 3.5))

# Erste Achse: Abfluss an den verschiedenen Messstellen
ax1.plot(Q3, color = "tab:green", label = r"$Q_{\mathrm{M3}}$")
ax1.plot(Q4, color="tab:blue", label = r"$Q_{\mathrm{M4}}$")
ax1.plot(Q3GB_clean, color = "tab:red", label = r"$Q_{\mathrm{M3}}+Q_{\mathrm{GB}}$")
ax1.set_ylabel("Abfluss [m$^3$ s$^{-1}$]", color="tab:blue")
ax1.set_xlabel("Zeit")
ax1.tick_params(axis="x", rotation=45)
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.grid(True)
ax2 = ax1.twinx()
#ax2.plot (differenzQ3GBQ4_clean, color="tab:orange", label=r"Differenz ($\frac{Q_{\mathrm{MGB}}}{Q_{\mathrm{M4}}}$)")
ax2.plot (AnteilGB_clean, color="tab:orange", label=r"Anteil GB ($\frac{Q_{\mathrm{MGB}}}{Q_{\mathrm{M4}}}$)")
ax2.set_ylabel("Anteil [%]", color="tab:orange")
ax2.tick_params(axis="y", labelcolor="tab:orange")
# ax2.grid(True)

# gemeinsame Legende
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2
ax1.legend(handles, labels, loc = 'best')

fig.tight_layout()
fig.savefig('H1_AnteilGB.png', dpi=300)

print("Mittlere Differenz zwischen Q3+GB und Q4 [m^3/s]:", differenzQ3GBQ4_clean.mean())
