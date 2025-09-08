# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 17:26:43 2025

@author: Pauline Fesser & Lena Oker
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sig
from sklearn.linear_model import LinearRegression
from scipy import stats
import matplotlib.dates as mdates

# Einlesen der Daten 
# csv-Dateien einlesen
df = pd.read_csv("M1_Leitfaehigkeit.csv", delimiter=";")    # M1
df2 = pd.read_csv("M2_Leitfaehigkeit.csv", delimiter=";")   # M2
df3 = pd.read_csv("M3_Leitfaehigkeit.csv", delimiter=";")   # M3
df4 = pd.read_csv("M4_Leitfaehigkeit.csv", delimiter=";")   # M4

# datum zu datetime konvertieren für M1, M2 und M4
df['Zeit'] = pd.to_datetime(df['Datetime'], format="%d.%m.%Y %H:%M")    # M1
df2['Zeit'] = pd.to_datetime(df2['Datetime'], format="%d.%m.%Y %H:%M")  # M2
df4['Zeit'] = pd.to_datetime(df4['Datetime'], format="%d.%m.%Y %H:%M")  # M4
#df3['Zeit'] = pd.to_datetime(df3['Datetime'], format="%d.%m.%Y %H:%M")  # M4

# Datum + Uhrzeit zu datetime kombinieren für M3
df3['Zeit'] = pd.to_datetime(df3['Date'] + ' ' + df3['Time'], format="%d.%m.%Y %H:%M:%S")

# Plot der Leitfähigkeitsdaten
# Zeitraum festlegen
start1 = pd.to_datetime("08.08.2025 18:00", format="%d.%m.%Y %H:%M")
end1   = pd.to_datetime("13.08.2025 11:00", format="%d.%m.%Y %H:%M")

# festgelegten Zeitraum aus jedem Datensatz auswählen
df_plot  = df[(df['Zeit'] >= start1) & (df['Zeit'] <= end1)]    #M1
df2_plot = df2[(df2['Zeit'] >= start1) & (df2['Zeit'] <= end1)] #M2
df3_plot = df3[(df3['Zeit'] >= start1) & (df3['Zeit'] <= end1)] #M3
df4_plot = df4[(df4['Zeit'] >= start1) & (df4['Zeit'] <= end1)] #M4

# plot
plt.figure(figsize=(12,8))
plt.plot(df_plot['Zeit'], df_plot['Leitfaehigkeit_cor'], label='M1')
plt.plot(df2_plot['Zeit'], df2_plot['Leitfaehigkeit_cor'], label='M2')
plt.plot(df3_plot['Zeit'], df3_plot['Leitfaehigkeit_cor'], label='M3')
plt.plot(df4_plot['Zeit'], df4_plot['Leitfaehigkeit_cor'], label='M4')

# Uhrzeit anzeigen
ax = plt.gca() 
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M"))

# Labels drehen, damit sie lesbar sind
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

plt.xlabel("Zeit", fontsize=20)
plt.ylabel("Leitfähigkeit [µS/cm]", fontsize=20)
plt.tick_params(axis="both", labelsize=15)
plt.legend(fontsize=20)
plt.grid(True)
plt.show()

#%% Kreuzkorrelation
# Zeitraum für die Kreuzkorrelation festlegen 
start = pd.to_datetime("10.08.2025 11:58", format="%d.%m.%Y %H:%M")
end   = pd.to_datetime("11.08.2025 04:00", format="%d.%m.%Y %H:%M")

# festgelegten Zeitraum aus den Datensätzen der Messstellen auswählen
df_zeitraum  = df[(df['Zeit'] >= start) & (df['Zeit'] <= end)]      # M1
df2_zeitraum = df2[(df2['Zeit'] >= start) & (df2['Zeit'] <= end)]   # M2
df3_zeitraum = df3[(df3['Zeit'] >= start) & (df3['Zeit'] <= end)]   # M3
df4_zeitraum = df4[(df4['Zeit'] >= start) & (df4['Zeit'] <= end)]   # M4

# Leitfähigkeitsdaten aus den Datensätzen der Messstellen extrahieren
EC1 = df_zeitraum["Leitfaehigkeit_cor"].values  # M1
EC2 = df2_zeitraum["Leitfaehigkeit_cor"].values # M2
EC3 = df3_zeitraum["Leitfaehigkeit_cor"].values # M3
EC4 = df4_zeitraum["Leitfaehigkeit_cor"].values # M4

# Leitfähigkeitsdaten als Liste speichern
EC= [EC1, EC2, EC3, EC4]

# Vorbereitung Kreuzkorrelation
# Mittelwert abziehen
EC_centered1 = EC1 - np.mean(EC1) # M1
EC_centered2 = EC2 - np.mean(EC2) # M2
EC_centered3 = EC3 - np.mean(EC3) # M3
EC_centered4 = EC4 - np.mean(EC4) # M4

# Leitfähigkeitsdaten mit abgezogenem Mittelwert als Liste speichern
EC_centered = [EC_centered1, EC_centered2, EC_centered3, EC_centered4]

# Schleife für alle Messstellen
# Erstellen leeres dictionary
cov = {}            # Kovarianz
lags = {}           # Anzahl der Verschiebungen, um die das Signal für die Kreuzkorrelation verschoben wird
                    # eine Verschiebung entspricht 5 Minuten (Messabstände sind 5 Minuten)
lag_max = {}        # Anzahl der Verschiebungen mit maximaler Korrelation
time_shift_sec = {} # Zeitverschiebung

# zeitlicher Abstand zwischen den Messpunkten
dt = 5*60  # 5 Minuten

for MS in range(3):
    # Berechnung Kovarianz
    cov[MS] = sig.correlate(EC_centered[MS+1], EC_centered[MS], mode="full")
    
    # Berechnung Korrelationskoeffizient
    cov_norm = cov[MS] / (np.std(EC_centered[MS]) * np.std(EC_centered[MS+1]) * len(EC_centered[MS]))
    r_max = np.max(cov_norm)  # höchster Korrelationskoeffizient
    print(f"Max. Korrelationskoeffizient M{MS+1} & M{MS+2}: {r_max:.3f}")

    # Berechnung Anzahl der Verschiebungen 
    lags[MS] = np.arange(-len(EC[MS+1]) + 1, len(EC[MS+1]))

    # Anzahl der Verschiebungen mit maximaler Korrelation
    lag_max[MS] = lags[MS][np.argmax(cov[MS])]
    print(f"Anzahl der Verschiebungen Messstellen {MS+1} & {MS+2}: {lag_max[MS]}")
    
    # Berechnung Zeitverschiebung
    time_shift_sec[MS] = lag_max[MS] * dt
    time_shift_min = time_shift_sec[MS] / 60
    print(f"Zeitverschiebung: {time_shift_sec[MS]} Sekunden / {time_shift_min:.1f} Minuten")

    # Plot
    plt.figure(figsize=(10,4))
    plt.plot(lags[MS], cov_norm)  
    plt.axvline(lag_max[MS], color='r', linestyle='--',
                label=f"Korrelationskoeffizient = {r_max:.3f}, Lag = {time_shift_min:.1f} min")
    plt.xlabel("Lag (Anzahl Verschiebungen)")
    plt.ylabel("Korrelationskoeffizient")
    plt.title(f"Kreuzkorrelation M{MS+1} & M{MS+2}")
    plt.legend()
    plt.show()

