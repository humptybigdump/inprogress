#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

df1 =  pd.read_csv("Felddaten Logger 1.txt")
df2 =  pd.read_csv("Felddaten Logger 2.txt")
df3 =  pd.read_csv("Felddaten Logger 3.txt")
df4 =  pd.read_csv("Felddaten Logger 4.txt")

print(df1.columns)

df1["Time"] = pd.to_datetime(df1["Time (sec)"], unit="s")
df2["Time"] = pd.to_datetime(df2["Time (sec)"], unit="s")
df3["Time"] = pd.to_datetime(df3["Time (sec)"], unit="s")
df4["Time"] = pd.to_datetime(df4["Time (sec)"], unit="s")
print(df1[["Time (sec)", "Time"]].head())


start = pd.Timestamp('2025-08-04')
ende = pd.Timestamp('2025-08-17 23:59:59') # Daten vom 4. bis 17. August
df1 = df1[(df1['Time'] >= start) & (df1['Time'] <= ende)]
df2 = df2[(df2['Time'] >= start) & (df2['Time'] <= ende)]
df3 = df3[(df3['Time'] >= start) & (df3['Time'] <= ende)]
df4 = df4[(df4['Time'] >= start) & (df4['Time'] <= ende)]
print("df1 Länge:", len(df1))
print("df2 Länge:", len(df2))
print("df3 Länge:", len(df3))
print("df4 Länge:", len(df4))


# In[6]:


#Temperaturdaten während des Tracerversuchs mitteln

tracerstart_unix  = 1754855460 #21.51 Uhr (Tracerzugabe)
tracerende_unix   = 1754871300 # 02.15 Uhr (letzte Probe)

#Datenteil im Zeitraum während dem Tracerversuch ermitteln 
idx_tracerstart1 = df1.index[df1['Time (sec)']==tracerstart_unix].item()
idx_tracerende1  = df1.index[df1['Time (sec)']==tracerende_unix].item()
idx_tracerstart2 = df2.index[df2['Time (sec)']==tracerstart_unix].item()
idx_tracerende2  = df2.index[df2['Time (sec)']==tracerende_unix].item()
idx_tracerstart3 = df3.index[df3['Time (sec)']==tracerstart_unix].item()
idx_tracerende3  = df3.index[df3['Time (sec)']==tracerende_unix].item()
idx_tracerstart4 = df4.index[df4['Time (sec)']==tracerstart_unix].item()
idx_tracerende4  = df4.index[df4['Time (sec)']==tracerende_unix].item()


#zur Betrachtung der Messabschnitte: jeweils Start- und Endmessstelle des Abschnitts in eine Variable schreiben
temperatur_MS1_2_ges = np.array(df1['T (deg C)'][idx_tracerstart1:idx_tracerende1], df2['T (deg C)'][idx_tracerstart2:idx_tracerende2])
temperatur_MS2_3_ges = np.array(df2['T (deg C)'][idx_tracerstart2:idx_tracerende2], df3['T (deg C)'][idx_tracerstart3:idx_tracerende3])
temperatur_MS3_4_ges = np.array(df3['T (deg C)'][idx_tracerstart3:idx_tracerende3], df4['T (deg C)'][idx_tracerstart4:idx_tracerende4])

#Spannweite der Temperaturen
T_MS1_2_range = max(temperatur_MS1_2_ges)- min(temperatur_MS1_2_ges)
T_MS2_3_range = max(temperatur_MS2_3_ges)- min(temperatur_MS2_3_ges)
T_MS3_4_range = max(temperatur_MS3_4_ges)- min(temperatur_MS3_4_ges)

TemperaturMS1_2_mean = np.mean(temperatur_MS1_2_ges)
TemperaturMS2_3_mean = np.mean(temperatur_MS2_3_ges)
TemperaturMS3_4_mean = np.mean(temperatur_MS3_4_ges)

TemperaturMS1_2_std  = np.std(temperatur_MS1_2_ges)
TemperaturMS2_3_std  = np.std(temperatur_MS2_3_ges)
TemperaturMS3_4_std  = np.std(temperatur_MS3_4_ges)

print("mittlere Temperaturen in den Abschnitten:")
print(f"MS1_2: {TemperaturMS1_2_mean:.3f} (± {TemperaturMS1_2_std:.3f}) Grad Celsius; Range: {T_MS1_2_range:.3f}°C")
print(f"MS2_3: {TemperaturMS2_3_mean:.3f} (± {TemperaturMS2_3_std:.3f}) Grad Celsius; Range: {T_MS2_3_range:.3f}°C")
print(f"MS3_4: {TemperaturMS3_4_mean:.3f} (± {TemperaturMS3_4_std:.3f}) Grad Celsius; Range: {T_MS3_4_range:.3f}°C")



# In[9]:


#Tagesgang von k2


# Tagesgang berechnen (Mittelwerte pro Stunde)
def tagesgang(df):
    df['Hour'] = df['Time'].dt.hour  # nur Stunde extrahieren
    return df.groupby('Hour')['T (deg C)'].mean() #Temperaturmittelwert pro Stunde

tg1 = tagesgang(df1) #Tagesgänge Temperaturen in °C an den Messstellen
tg2 = tagesgang(df2)
tg3 = tagesgang(df3)
tg4 = tagesgang(df4)

tgMS1_2_mean = (tg1 + tg2) /2 #gemittelter Temperatur-Tagesgang für die Messabschnitte
tgMS2_3_mean = (tg2 + tg3) /2 
tgMS3_4_mean = (tg3 + tg4) /2


#aus anderem Code: k2_Sauerstoff auf andere Temperaturen umrechnen
# Einheit: 1/min
k2_MS1_2_O2 = 0.018
k2_MS2_3_O2 = 0.020
k2_MS3_4_O2 = 0.017


#Temperaturumrechnung nicht auf 20 Grad, sondern auf Tagesgang-Temperaturen für jeweiligen Abschnitt
#k2_Tagesgang = k2(T) /1.0241^(T-Tagesgang)
k2_MS1_2_tg = k2_MS1_2_O2/(1.0241**(TemperaturMS1_2_mean-tgMS1_2_mean))
k2_MS2_3_tg = k2_MS2_3_O2/(1.0241**(TemperaturMS2_3_mean-tgMS2_3_mean))
k2_MS3_4_tg = k2_MS3_4_O2/(1.0241**(TemperaturMS3_4_mean-tgMS3_4_mean))
#spannweite der k2 über den Tag
k2_MS1_2_tg_range = max(k2_MS1_2_tg) - min(k2_MS1_2_tg)
k2_MS2_3_tg_range = max(k2_MS2_3_tg) - min(k2_MS2_3_tg)
k2_MS3_4_tg_range = max(k2_MS3_4_tg) - min(k2_MS3_4_tg)
print(f"range MS1_2: {k2_MS1_2_tg_range:.4f}")
print(f"range MS2_3: {k2_MS2_3_tg_range:.4f}")
print(f"range MS3_4: {k2_MS3_4_tg_range:.4f}")



# Plotten von Temperatur und Gasaustauschkoeffizienten Tagesgang
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(k2_MS1_2_tg.index, k2_MS1_2_tg.values, color='#F58514', marker='o', label='Messstelle 1 bis 2')
ax1.plot(k2_MS2_3_tg.index, k2_MS2_3_tg.values, color='#00A37A', marker='o', label='Messstelle 2 bis 3')
ax1.plot(k2_MS3_4_tg.index, k2_MS3_4_tg.values, color='#FF5CE2', marker='o', label='Messstelle 3 bis 4')

#ax2 = ax1.twinx()
#ax2.fill_between(tgMS1_2_mean.index, tgMS1_2_mean.values, alpha=0.2, color='#F58514', label='Temperatur (MS 1–2)')
#ax2.fill_between(tgMS2_3_mean.index, tgMS2_3_mean.values, alpha=0.2, color='#00A37A', label='Messstelle 2 bis 3')
#ax2.fill_between(tgMS3_4_mean.index, tgMS3_4_mean.values, alpha=0.2, color='#FF5CE2', label='Messstelle 3 bis 4')
#ax2.set_ylabel('Durchschnittliche Temperatur [°C]')

plt.xlabel('Stunde des Tages')
ax1.set_ylabel('Gasaustauschkoeffizient in 1/min')
plt.xticks(range(0,24))  # alle Stunden anzeigen
plt.grid(True, alpha=0.3)
plt.legend(title='Messstellen')
plt.show()


# In[4]:


# Plotten


# In[ ]:




