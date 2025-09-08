# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 11:55:35 2025

@author: Pauline Fesser und Lena Oker
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# CSV-Dateien mit den unbereinigten Tracerdaten einlesen
df = pd.read_csv("F01_korrigiert.csv", delimiter=";")  #Fluorometer 1 (M1 und M3)
df2 = pd.read_csv("F02_korrigiert.csv", delimiter=";") # Fluorometer 2 (M2 und M4)

# Datum + Uhrzeit zu datetime kombinieren
df['Zeit'] = pd.to_datetime(df['Datum'] + ' ' + df['Uhrzeit'], format="%m.%d.%Y %H:%M:%S")
df2['Zeit'] = pd.to_datetime(df2['Datum'] + ' ' + df2['Uhrzeit'], format="%m.%d.%Y %H:%M:%S")

# Plot der Messdaten gegen die Zeit 
plt.figure(figsize=(12,8))
plt.plot(df['Zeit'], df['Spannung2'], marker='.', linestyle='', label='Fluorometer 1')
plt.plot(df2['Zeit'], df2['Spannung2'], marker='.', linestyle='', label='Fluorometer 2')

# Zeit Tracerzugabe
zeit_in = np.datetime64('2025-08-10 21:50:25')

# Senkrechte Linie zur Zeit der Tracerzugabe
plt.axvline(x=zeit_in, color='black', linestyle='--', linewidth=2, label='Tracerzugabezeitpunkt')

# Uhrzeit an der x-Achse formatieren 
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M"))

# Labels drehen, damit sie lesbar sind
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

plt.xlabel("Zeit",fontsize=20)
plt.ylabel("Fluoreszenz [mV]", fontsize=20)
plt.tick_params(axis="both", labelsize=15)
plt.legend(fontsize=20)
plt.grid(True)
plt.show()