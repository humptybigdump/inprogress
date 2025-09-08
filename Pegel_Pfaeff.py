# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 11:15:58 2025

### Vergleich M3 und Pegel Pfäffingen ###

@author: Ellen Diez
"""
# =============================================================================
# 1. Daten einlesen
# =============================================================================

# Pakete importieren
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels. api as sm
from datetime import timedelta
import matplotlib.dates as mdates

# Durchflusszeitreihe M3 einlesen
M3 = pd.read_csv('M3_Durchflusszeitreihe.csv')
M3['datetime'] = pd.to_datetime(M3['datetime'])

# Daten Pfäffingen einlesen und zuschneiden
PP = pd.read_csv('Q_Pegel_Pfaeffingen.csv', sep = ';', decimal = ',')
PP['datetime'] = pd.to_datetime(PP['Zeit [dd.mm.yyyy hh:mm]'], format = '%d.%m.%Y %H:%M')
ende = '2025-08-12 23:59:00'
PP = PP[PP['datetime'] <= ende]

# Ausreißer (entsprechend M3) entfernen
PP['Q [m^3/s]'].loc[PP['datetime'] == '2025-08-06 16:00:00'] = np.nan

# Datetimespalte als Index setzen
M3.set_index('datetime', inplace = True)
PP.set_index('datetime', inplace = True)

# Fünfzehnminütige Druck- und Luftdruckdaten extrahieren
M315 = M3[M3.index.minute % 15 == 0]
PP15 = PP[PP.index.minute % 15 == 0]

#%% ===========================================================================
# 2. Kreuzkorrelation durchführen und Maxlag bestimmen
# =============================================================================

# Q-Vektoren erstellen
QM3 = M315['Q_curve [m^3/s]']
QPP = PP15['Q [m^3/s]']

# Kreuzkorrelation der Durchflusszeitreihen berechnen
crosscor3P = sm.tsa.stattools.ccf(QM3.dropna(), QPP.dropna(), adjusted = True)

# Zeitverschiebungslimit --> # hiermit verhindern wir, dass zufällige Korrelationsmaxima, die später auftreten, berücksichtigt werden
lags = np.arange(len(crosscor3P))               # Lags entsprechen dem Index der Kreuzkorrelation
global_lag_limit = 180           
valid_lags = lags <= global_lag_limit
crosscor3P_trimmed = crosscor3P[valid_lags]     # beschränkte Kreuzkorrelation

# Ausgabe maximaler Korrelation
maxcor = crosscor3P_trimmed.max()               # maximale Kreuzkorrelation
maxlag = np.argmax(crosscor3P_trimmed)          # Verschiebung, bei der maximale Korrelation erreicht wird
print('\nKorrelationsmaximum M3/PP: ' + str(maxcor) + '\n(bei einer Verschiebung um ' + str(maxlag) + ' Zeitschritte je 15 Minuten)')

#%% ===========================================================================
# 3. Plot für Kreuzkorrelation erstellen
# =============================================================================

fig, ax1 = plt.subplots(1,2, figsize = (12,4))
ax1[0].plot(np.arange(len(crosscor3P_trimmed))*15, crosscor3P_trimmed)
#ax1[0].set_title("Kreuzkorrelation", fontsize = 25, pad = 14)
ax1[0].set_ylabel("Korrelation M3 und PP", fontsize = 18)
ax1[0].set_xlabel("Zeitverschiebung in Minuten", fontsize = 18)
ax1[0].grid()

# =============================================================================
# 4. Verschobene Zeitreihen und Verhältnis plotten
# =============================================================================

# Zeitverschiebung auf Zeitstempel Durchflusszeitreihe Pfäffingen addieren
delta = timedelta(hours = 4.75)
QPP_lag = QPP.copy()
QPP_lag.index = QPP_lag.index + delta
QPP_lag = QPP_lag[QPP_lag.index <= ende]    # Überstand nach hinten abschneiden
start2 = '2025-08-04 04:45:00'
QM3 = QM3[QM3.index >= start2]              # Überstand nach vorne abschneiden

# Quotienten und Mittelwert des Quotienten berechnen
quo = QM3/QPP_lag 
quo_mean = quo.mean()
print(f'Mittelwert Verhältnis: {quo_mean}')

# Differenz und Mittelwert der Differenz berechnen
dif = QM3 - QPP_lag
dif_mean = dif.mean()
print(f'Mittelwert Differenz: {dif_mean}')

# Plot erstellen
#fig, ax1 = plt.subplots()
ax1[1].plot(QM3, color = '0.2', linestyle = '-', label = 'Durchfluss M3')
ax1[1].plot(QPP_lag, color = '0.6' , linestyle = '-', label = 'Durchfluss Pegel (verschoben)')
#ax1.set_title('Durchflussverhältnisse', fontsize = 25, pad = 12)
ax1[1].set_xlabel('Zeit', fontsize = 18)
ax1[1].set_ylabel('Durchfluss $Q\ [\mathrm{[m^3\ s^{-1}]}]$', fontsize = 18)
ax1[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1[1].tick_params(axis = 'x', labelrotation = 45)
ax1[1].grid()

ax2 = ax1[1].twinx()
ax2.plot(quo, color = 'blue', alpha = 0.8, label = 'Verhältnis')
ax2.set_ylabel('Verhältnis M3/PP', fontsize = 18)
ax2.axhline(quo_mean, color = 'red', linestyle = '--', label = 'Mittelwert Verhältnis')

# gemeinsame Legende
handles1, labels1 = ax1[1].get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2
ax1[1].legend(handles, labels, loc = 'best')

# Abstände der Plots festlegen
plt.subplots_adjust(wspace = 0.25, hspace = 0.5)