#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 10:54:41 2025

@author: etiennebarbe
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


df1 =  pd.read_csv("Felddaten Logger 1.txt")
df2 =  pd.read_csv("Felddaten Logger 2.txt")
df3 =  pd.read_csv("Felddaten Logger 3.txt")
df4 =  pd.read_csv("Felddaten Logger 4.txt")
df5 =  pd.read_csv("Felddaten Logger 5.txt")
df6 =  pd.read_csv("Sonnenstation_blend.csv")
df7 =  pd.read_csv("Lufttemperatur.csv")


print(df1.columns)
print(df6.columns)


df1["Time"] = pd.to_datetime(df1["Time (sec)"], unit="s")
df2["Time"] = pd.to_datetime(df2["Time (sec)"], unit="s")
df3["Time"] = pd.to_datetime(df3["Time (sec)"], unit="s")
df4["Time"] = pd.to_datetime(df4["Time (sec)"], unit="s")
df5["Time"] = pd.to_datetime(df5["Time (sec)"], unit="s")
df6["Time"] = pd.to_datetime(df6['timestamp'])
df7["Time"] = pd.to_datetime(df7['time'])


print(df1[["Time (sec)", "Time"]].head())


start = pd.Timestamp('2025-08-04')
ende = pd.Timestamp('2025-08-17 23:59:59') #welcher Zeitrahmen?
df1 = df1[(df1['Time'] >= start) & (df1['Time'] <= ende)]
df2 = df2[(df2['Time'] >= start) & (df2['Time'] <= ende)]
df3 = df3[(df3['Time'] >= start) & (df3['Time'] <= ende)]
df4 = df4[(df4['Time'] >= start) & (df4['Time'] <= ende)]
df5 = df5[(df5['Time'] >= start) & (df5['Time'] <= ende)]


print("df1 Länge:", len(df1))
print("df2 Länge:", len(df2))
print("df3 Länge:", len(df3))
print("df4 Länge:", len(df4))
print("df5 Länge:", len(df5))


## Plot über Zeit mit 5 Messstellen
## Plot über Zeit mit 5 Messstellen
fig, ax1 = plt.subplots(figsize=(10,6))

# Temperaturen (nur auf ax1)
ax1.scatter(df1["Time"], df1["T (deg C)"], color='red', marker='x', s=1, alpha=0.7, label="Messstelle 1")
ax1.scatter(df2["Time"], df2["T (deg C)"], color='orange', marker='x', s=1, alpha=0.7, label="Messstelle 2")
ax1.scatter(df3["Time"], df3["T (deg C)"], color='blue', marker='x', s=1, alpha=0.7, label="Messstelle 3")
ax1.scatter(df4["Time"], df4["T (deg C)"], color='skyblue', marker='x', s=1, alpha=0.7, label="Messstelle 4")
ax1.scatter(df5["Time"], df5["T (deg C)"], color='green', marker='x', s=1, alpha=0.7, label="Goldersbach")
ax1.scatter(df7["Time"], df7["temp"], color='black', marker='*', s=1, alpha=0.7, label="Lufttemperatur")

ax1.set_xlabel('Datum')
ax1.set_ylabel('Temperatur [°C]', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, alpha=0.3)

# Strahlung NUR auf ax2
ax2 = ax1.twinx()
ax2.plot(df6['Time'], df6['S1_plot_blended'], 
         color='violet', marker='x', linestyle='--', alpha=0.7, label='Strahlung Sonnenstation')
ax2.set_ylabel('Strahlung [W m^{-2}]', color='violet')
ax2.tick_params(axis='y', colors='violet')

# Legende kombinieren
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', title='Messstellen')

plt.title("Temperaturdynamik an den 5 Messstellen und Strahlung an der Sonnenstation")
plt.tight_layout()
plt.show()


## Boxplots für jede Messtelle

data = pd.DataFrame({
    "Messstelle 1": df1["T (deg C)"],
    "Messstelle 2": df2["T (deg C)"],
    "Messstelle 3": df3["T (deg C)"],
    "Messstelle 4": df4["T (deg C)"],
    "Messstelle 5": df5["T (deg C)"],
})

# Boxplot direkt mit Pandas
plt.figure(figsize=(10,6))
data.boxplot()
plt.ylabel("Temperatur (°C)")
plt.title("Temperaturverteilung an 5 Messstellen")
plt.show()


# Tagesgang Temperatur
def tagesgang_temp(df):
    df['Hour'] = df['Time'].dt.hour
    return df.groupby('Hour')['T (deg C)'].mean()

tg1 = tagesgang_temp(df1)
tg2 = tagesgang_temp(df2)
tg3 = tagesgang_temp(df3)
tg4 = tagesgang_temp(df4)
tg5 = tagesgang_temp(df5)

# Tagesgang Strahlung
df6['timestamp'] = pd.to_datetime(df6['timestamp'])  # WICHTIG
df6['Hour'] = df6['timestamp'].dt.hour
tg6 = df6.groupby('Hour')['S1_plot_blended'].mean()

df7['Time'] = pd.to_datetime(df7['time'])  # WICHTIG
df7['Hour'] = df7['Time'].dt.hour
tg7 = df7.groupby('Hour')['temp'].mean()

# Plot
fig, ax1 = plt.subplots(figsize=(10,6))

# Temperaturkurven
ax1.plot(tg1.index, tg1.values, color='red', marker='o', label='Messstelle 1')
ax1.plot(tg2.index, tg2.values, color='orange', marker='o', label='Messstelle 2')
ax1.plot(tg3.index, tg3.values, color='blue', marker='o', label='Messstelle 3')
ax1.plot(tg4.index, tg4.values, color='skyblue', marker='o', label='Messstelle 4')
ax1.plot(tg5.index, tg5.values, color='green', marker='o', label='Goldersbach')
ax1.plot(tg7.index, tg7.values, color='violet', marker='x', label='Lufttemperatur')
ax1.set_xlabel('Zeit in Stunden (MESZ)')
ax1.set_ylabel('Temperatur [°C]')
ax1.set_xticks(range(0,24))
ax1.grid(True, alpha=0.3)

# Zweite y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(tg6.index, tg6.values, color='black', marker='x', linestyle='--', label='Strahlung Sonnenstation')
ax2.set_ylabel('Strahlung [W/m$^2$]')
ax2.tick_params(axis='y', colors='black')

# Legende kombinieren
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', title='Messstellen')

plt.title('Tagesgang der Temperaturmittelwerte mit Strahlungsdaten')
plt.show()