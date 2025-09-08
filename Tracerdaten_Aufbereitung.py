# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 18:41:56 2025

@author: Pauline Fesser und Lena Oker
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# csv Dateien einlesen
df = pd.read_csv("M1_Tracerdaten.csv", delimiter=";")          # M1
df2 = pd.read_csv("M2_Tracerdaten.csv", delimiter=";") # M2
df3 = pd.read_csv("M3_Tracerdaten.csv", delimiter=";")              # M3
df4 = pd.read_csv("M4_Tracerdaten.csv", delimiter=";") # M4

# Einlesen csv Datei der Handproben
data_hand = pd.read_csv('Handproben.csv', sep=';')

# Datum und Uhrzeit zu datetime kombinieren
df['Zeit'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format="%m.%d.%Y %H:%M:%S")
df2['Zeit'] = pd.to_datetime(df2['Date'] + ' ' + df2['Time'], format="%m.%d.%Y %H:%M:%S")
df3['Zeit'] = pd.to_datetime(df3['Date'] + ' ' + df3['Time'], format="%m.%d.%Y %H:%M:%S")
df4['Zeit'] = pd.to_datetime(df4['Date'] + ' ' + df4['Time'], format="%m.%d.%Y %H:%M:%S")

# lineare Interpolation für Messstelle 2 und 4
df2['c'] = df2['c'].interpolate(method='linear')
df4['c'] = df4['c'].interpolate(method='linear')

# Start- und Endzeit als Datetime (Zeitraum der Messdaten)
start = pd.Timestamp("2025-08-10 21:50:25")
end   = pd.Timestamp("2025-08-11 2:50:25")

# Erzeugen einer Zeitreihe im 5-Sekunden-Abstand
zeit_neu = pd.date_range(start, end, freq="5S")

# Zeit Tracerzugabe
zeit_in = np.datetime64('2025-08-10 21:50:25')

# Zeit seit Zugabe in Stunden
t_in_h=(zeit_neu-zeit_in).total_seconds()/3600.

# Ergänzung Zeit seit Zugabe in Stunden im Dataframe
df['t_in_h'] = (df['Zeit'] - zeit_in) / np.timedelta64(1, 'h')      # M1
df2['t_in_h'] = (df2['Zeit'] - zeit_in) / np.timedelta64(1, 'h')    # M2
df3['t_in_h'] = (df3['Zeit'] - zeit_in) / np.timedelta64(1, 'h')    # M3
df4['t_in_h'] = (df4['Zeit'] - zeit_in) / np.timedelta64(1, 'h')    # M4

# Zeitachsen in float konvertieren für Messtelle 2 und 4
zeit_neu_float = zeit_neu.values.astype("datetime64[s]").astype(float)
t_daten2 = df2['Zeit'].values.astype("datetime64[s]").astype(float)
t_daten4 = df4['Zeit'].values.astype("datetime64[s]").astype(float)

# Korrektur der Basiskonzentration an Messtelle 2, 3 und 4
# Definition der trendremoval Funktion
def trendremoval(t_low, t_high, t_in_h, c):

    c_low=np.mean(c [t_in_h<=t_low])    # Mittelwert der Basiskonzentration vor Konzentrationsanstieg

    c_high=np.mean(c [t_in_h>=t_high])  # Mittelwert der Basiskonzentration nach Konzentrationsabfall 

    trend =np.ones(len(c))*c_low        
    
# Zeitbereich zwischen den Basiskonzentrationen definieren und Trendberechnung in diesem Zeitbereich durchführen (Steigung)
    mask_middle = (t_in_h > t_low) & (t_in_h < t_high)
    trend[mask_middle] = c_low + (c_high - c_low)/(t_high - t_low) * (t_in_h [mask_middle] - t_low)                           
                                       
    trend[t_in_h>=t_high]=c_high
    
# Berechnung der korrigierten Konzentration
    c_cor=c-trend
    
    return c_cor

# Aufruf der trendremoval Funktion für Messtelle 2, 3 und 4
c_cor2=trendremoval(1.12083, 2.34722, df2['t_in_h'], df2['c'])
df2['c_cor']=c_cor2
c_cor3=trendremoval(2.21361, 3.57889, df3['t_in_h'], df3['c'])
df3['c_cor']=c_cor3
c_cor4=trendremoval(2.96417, 4.50167, df4['t_in_h'], df4['c'])
df4['c_cor']=c_cor4

# Extrapolation aller 4 Messtellen
konz_interp1 = np.interp(zeit_neu, df['Zeit'], df['c2'],left=0,right=0)
konz_interp2 = np.interp(zeit_neu_float, t_daten2, df2['c_cor'],left=0,right=0)
konz_interp3 = np.interp(zeit_neu, df3['Zeit'], df3['c_cor'],left=0,right=0)
konz_interp4 = np.interp(zeit_neu_float, t_daten4, df4['c_cor'],left=0,right=0)

# Erstellung neuer Datensatz mit korrigierter Konzentration und Zeit
df_neu = pd.DataFrame({
    'Datetime': zeit_neu,
    't_in_h': t_in_h, 
    'c1': konz_interp1,
    'c2': konz_interp2,
    'c3': konz_interp3,
    'c4': konz_interp4,
})

# Exportieren des neuen Datensatzes als txt Datei (auskommentieren bei Bedarf)
# df_neu.to_csv("tracerdaten_cor_1.txt", sep=";", index=False)

# Datum und Uhrzeit zu datetime kombinieren für die Handprobenmessungen
data_hand['Zeit1'] = pd.to_datetime(data_hand['M1_date'] + ' ' + data_hand['M1_time'], format="%d.%m.%Y %H:%M:%S")
data_hand['Zeit2'] = pd.to_datetime(data_hand['M2_date'] + ' ' + data_hand['M2_time'], format="%d.%m.%Y %H:%M:%S")
data_hand['Zeit3'] = pd.to_datetime(data_hand['M3_date'] + ' ' + data_hand['M3_time'], format="%d.%m.%Y %H:%M:%S")
data_hand['Zeit4'] = pd.to_datetime(data_hand['M4_date'] + ' ' + data_hand['M4_time'], format="%d.%m.%Y %H:%M:%S")

# Plot Messstellen mit Uhrzeiten auf der x-Achse
plt.figure(figsize=(12,8))
plt.plot(zeit_neu, konz_interp1, label='M1', marker='.', linestyle='')
plt.plot(zeit_neu, konz_interp2, label='M2', marker='.', linestyle='')
plt.plot(zeit_neu, konz_interp3, label='M3', marker='.', linestyle='')
plt.plot(zeit_neu, konz_interp4, label='M4', marker='.', linestyle='')

# Plot der Handprobenmessungen als Kreuze
plt.plot(data_hand['Zeit1'],data_hand['M1_c'],color='black', marker='x', linestyle='', label='Handproben')
plt.plot(data_hand['Zeit2'],data_hand['M2_c'],color='black', marker='x', linestyle='')
plt.plot(data_hand['Zeit3'],data_hand['M3_c'],color='black', marker='x', linestyle='')
plt.plot(data_hand['Zeit4'],data_hand['M4_c'],color='black', marker='x', linestyle='')

# Senkrechte Linie zur Zeit der Tracerzugabe
plt.axvline(x=zeit_in, color='black', linestyle='--', linewidth=2, label='Tracerzugabezeitpunkt')

# Uhrzeit anzeigen
ax = plt.gca() 
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M"))

# Labels drehen, damit sie lesbar sind
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

plt.xlabel("Zeit", fontsize=20)
plt.ylabel("Konzentration [µg/L]", fontsize=20)
plt.tick_params(axis="both", labelsize=15)
plt.legend(fontsize=20)
plt.grid(True)
plt.show()
