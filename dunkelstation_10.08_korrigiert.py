#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 15:42:37 2025

@author: jule
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from pandas import Timedelta
import math
import matplotlib.patches as mpatches

# === CSV-Datei einlesen ===================================================================
# Pfad zur CSV-Datei
csvfile_dunkel = "dunkelstation_roh.csv"
csvfile_sonne="sonnenstation_korrigiert_1min.csv"

# CSV einlesen
# Falls Datei Semikolons statt Kommas als Trennzeichen hat, sep=";" verwenden
df_raw_dunkel = pd.read_csv(csvfile_dunkel, sep=",")  
df_raw_sonne = pd.read_csv(csvfile_sonne, sep=",")
# Führende und abschließende Leerzeichen aus allen Spaltennamen entfernen
df_raw_dunkel.columns = df_raw_dunkel.columns.str.strip()
df_raw_sonne.columns = df_raw_sonne.columns.str.strip()

# Zeitstempel in datetime umwandeln(UTC)
df_raw_dunkel["Zeitstempel"] = pd.to_datetime(df_raw_dunkel["Zeitstempel"])
df_raw_sonne["timestamp"] = pd.to_datetime(df_raw_sonne["timestamp"])

#damit  das funktioniert mit den Zeitstempeln
df_raw_dunkel["Zeitstempel"] = pd.to_datetime(df_raw_dunkel["Zeitstempel"]).dt.tz_localize(None)
df_raw_sonne["timestamp"] = pd.to_datetime(df_raw_sonne["timestamp"]).dt.tz_localize(None)

# === In Langformat bringen: time, sensor, value ===
data = []

# Dunkelstation
for _, row in df_raw_dunkel.iterrows():
    ts = row["Zeitstempel"]
    data.append((ts, "Dunkelstation_1", row["Strahlung_S1mittel"]))
    data.append((ts, "Dunkelstation_2", row["Strahlung_S2mittel"]))

# Sonnenstation
for _, row in df_raw_sonne.iterrows():
    ts = row["timestamp"]
    data.append((ts, "Sonnenstation_1", row["S1_plot_blended"]))
    data.append((ts, "Sonnenstation_2", row["S2_plot_blended"]))

# === DataFrame erstellen ===
df = pd.DataFrame(data, columns=["time", "sensor", "value"])

# === Sortieren (wichtig!) ===
df.sort_values(["sensor", "time"], inplace=True)

# === Datenlücken > 5 min mit NaN markieren ===
max_gap = timedelta(minutes=5)

# === NaN-Lücken effizient einfügen (vectorisiert) ===
def insert_nans(group, max_gap=timedelta(minutes=5)):
    group = group.sort_values("time").reset_index(drop=True)
    time_diff = group["time"].diff()
    nan_rows = group[time_diff > max_gap].copy()
    nan_rows["time"] = nan_rows["time"] - time_diff[time_diff > max_gap]/2
    nan_rows["value"] = float('nan')
    return pd.concat([group, nan_rows]).sort_values("time").reset_index(drop=True)

df_prepared = df.groupby("sensor", group_keys=False).apply(insert_nans)
    
print(f"📊 Ursprüngliche Daten: {len(df)} Zeilen")
print(f"📊 Mit NaN-Lücken:      {len(df_prepared)} Zeilen")

# === Filter für Dunkelstation Sensor 1 & 2 ===
sensoren = ["Dunkelstation_1", "Dunkelstation_2", "Sonnenstation_1", "Sonnenstation_2"]
df_plot_tagesverlauf = df_prepared[df_prepared["sensor"].isin(sensoren)].copy()

#filtern sodass nur der eine Tag im df ist (zeitsparend)
start_day = "2025-08-10"
end_day = "2025-08-10 23:59:59"
df_plot_tagesverlauf = df_plot_tagesverlauf[(df_plot_tagesverlauf["time"] >= start_day) & (df_plot_tagesverlauf["time"] <= end_day)]

# === Zeitbasierte Glättung (30 Minuten) ===
df_plot_tagesverlauf = df_plot_tagesverlauf.copy()

# Index auf Zeit setzen, damit rolling("30min") funktioniert
df_plot_tagesverlauf = df_plot_tagesverlauf.set_index("time")

#alles glätten
df_plot_tagesverlauf["value_smooth"] = (
    df_plot_tagesverlauf.groupby("sensor")["value"]
    .transform(lambda x: x.rolling("10min", min_periods=1).mean())
) 

# Original-NaNs auch in value_smooth übernehmen
df_plot_tagesverlauf.loc[df_plot_tagesverlauf["value"].isna(), "value_smooth"] = float("nan")

# Zeit zurück als normale Spalte (praktisch für Plotten)
df_plot_tagesverlauf = df_plot_tagesverlauf.reset_index()

#df für rohdatenplot
dunkelsensor= ["Dunkelstation_1", "Dunkelstation_2"]
df_plot_dunkel=df_plot_tagesverlauf[df_plot_tagesverlauf["sensor"].isin(dunkelsensor)].copy()
# === Zeitbasierte Glättung (30 Minuten) ===
df_plot_dunkel = df_plot_dunkel.copy()

# Index auf Zeit setzen, damit rolling("30min") funktioniert
df_plot_dunkel = df_plot_dunkel.set_index("time")

#alles glätten
df_plot_dunkel["value_smooth"] = (
    df_plot_dunkel.groupby("sensor")["value"]
    .transform(lambda x: x.rolling("10min", min_periods=1).mean())
) 

# Original-NaNs auch in value_smooth übernehmen
df_plot_dunkel.loc[df_plot_dunkel["value"].isna(), "value_smooth"] = float("nan")

# Zeit zurück als normale Spalte (praktisch für Plotten)
df_plot_dunkel = df_plot_dunkel.reset_index()
#Plot dunkelstation

sensor1highlights = [
    ("07:35", "08:35"),
    ("09:30", "11:25"),
    ("15:50", "18:25")
]
sensor2highlights = [
    ("09:40", "11:40"),
    ("15:45", "18:20")
]
ax = plt.gca()  
fig, ax9 = plt.subplots(figsize=(12,6))
# Sensoren zeichnen
for sensor_name, group in df_plot_dunkel.groupby("sensor"):
    if sensor_name == "Dunkelstation_1":
        label = "DO"
        color = "orange"
    elif sensor_name == "Dunkelstation_2":
        label = "DU"
        color = "blue"
    else:
        label = sensor_name
    ax9.plot(group["time"], group["value_smooth"], label=label, color=color)
ax9.set_ylabel("Strahlung (W/m²)")
ax9.set_xlabel("Zeit (MESZ)")
#ax9.set_title("Tagesverlauf der Strahlungswerte der Dunkelstation am 10.08.2025")
ax9.legend()
ax9.grid(True)
ax9.set_xlim(pd.Timestamp("2025-08-10 00:00"),
             pd.Timestamp("2025-08-11 00:00"))
ax9.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax9.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M"))
ax9.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0,15,30,45]))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()


highlight_date = "2025-08-10"
# Bereiche für Sensor 1
for start, end in sensor1highlights:
    ax9.axvspan(pd.Timestamp(f"{highlight_date} {start}"),
                pd.Timestamp(f"{highlight_date} {end}"),
                color="orange", alpha=0.2)

# Bereiche für Sensor 2
for start, end in sensor2highlights:
    ax9.axvspan(pd.Timestamp(f"{highlight_date} {start}"),
                pd.Timestamp(f"{highlight_date} {end}"),
                color="blue", alpha=0.2)
    
# Dummy-Patches für die Legende hinzufügen
highlight1_patch = mpatches.Patch(color="orange", alpha=0.2, label="DO kein Schatten")
highlight2_patch = mpatches.Patch(color="blue", alpha=0.2, label="DU kein Schatten")

# Legende mit allen Handles
handles, labels = ax9.get_legend_handles_labels()
handles.extend([highlight1_patch, highlight2_patch])
ax9.legend(handles=handles, loc="upper left")    
plt.show()



cut = {
    "Dunkelstation_1": sensor1highlights,
    "Dunkelstation_2": sensor2highlights
}

day = "2025-08-10"
for sensor, intervals in cut.items():
    for start_str, end_str in intervals:
        start = datetime.strptime(f"{day} {start_str}", "%Y-%m-%d %H:%M")
        end   = datetime.strptime(f"{day} {end_str}", "%Y-%m-%d %H:%M")
        # NaN in value_smooth setzen = Daten „ausschneiden“
        mask = (df_plot_tagesverlauf["sensor"] == sensor) & (df_plot_tagesverlauf["time"] >= start) & (df_plot_tagesverlauf["time"] <= end)
        df_plot_tagesverlauf.loc[mask, "value_smooth"] = float("nan")
   
# --- 1-Minuten-Raster je Sensor (mean) mit komplettem Tagesindex ---
full_min_idx = pd.date_range(start=start_day, end=end_day, freq="1min")

dfs = []
for sensor, g in df_plot_tagesverlauf.groupby("sensor"):
    # auf Minuten mitteln
    gm = (g.set_index("time")
            .resample("1min")["value_smooth"]
            .mean()
            .reindex(full_min_idx))  # Lücken auf vollständigen Minutenraster ausdehnen (NaN)
    gm = gm.rename_axis("time").to_frame("value_smooth")
    gm["sensor"] = sensor
    dfs.append(gm.reset_index())

df_plot_tagesverlauf = pd.concat(dfs, ignore_index=True)

# --- Pivot aus der 1-Minuten-Serie aufbauen ---
df_pivot = df_plot_tagesverlauf.pivot(index="time", columns="sensor", values="value_smooth")

# --- k zunächst roh berechnen (tagsüber + nachts) ---
k_raw = -(np.log(df_pivot["Sonnenstation_2"] / df_pivot["Sonnenstation_1"])) / 0.31

# Nachtmaske (deine Zeiten beibehalten)
def is_night(ts):
    t = ts.time()
    return (t >= datetime.strptime("20:49", "%H:%M").time()) or (t <= datetime.strptime("06:09", "%H:%M").time())

night_mask = df_pivot.index.map(is_night)

# --- k mit Nachtmaskierung (nachts NaN) ---
df_pivot["k_wert"] = k_raw.mask(night_mask)

# --- SonneS2_Tiefe18 NUR berechnen, wenn k und S1 existieren; sonst NaN ---
df_pivot["SonneS2_Tiefe18"] = np.where(
    df_pivot["k_wert"].notna() & df_pivot["Sonnenstation_1"].notna(),
    df_pivot["Sonnenstation_1"] * np.exp(-df_pivot["k_wert"] * 0.18),
    np.nan
)

#Verhältnis===============================================
df_pivot = df_pivot.reset_index()

df_pivot['ratio_s1']=df_pivot["Dunkelstation_1"]/df_pivot["Sonnenstation_1"]
df_pivot['ratio_s2']=df_pivot["Dunkelstation_2"]/df_pivot["SonneS2_Tiefe18"]

# nur Zeiten zwischen 06:00 und 21:00 Uhr behalten
def is_daytime(ts):
    t = ts.time()
    return t >= datetime.strptime("06:09", "%H:%M").time() and t <= datetime.strptime("20:49", "%H:%M").time()

df_pivot.loc[~df_pivot["time"].apply(is_daytime), "ratio_s1"] = float("nan")
df_pivot.loc[~df_pivot["time"].apply(is_daytime), "ratio_s2"] = float("nan")

# === Mittelwerte der Verhältnisse berechnen ===
mean_ratio_s1 =df_pivot['ratio_s1'].mean(skipna=True)
mean_ratio_s2 = df_pivot['ratio_s2'].mean(skipna=True)

print("📈 Mittelwerte der Verhältnisse am 10.08.2025:")
print(f"   S1 (Dunkel/Sonne) = {mean_ratio_s1:.3f}")
print(f"   S2 (Dunkel/Sonne) = {mean_ratio_s2:.3f}")


#neue DunkelstationWerte mithilfe Verhältnisse berechnen
df_pivot['Dunkelstation_1_Neu']=df_pivot['Sonnenstation_1']*mean_ratio_s1
df_pivot['Dunkelstation_2_Neu']=df_pivot['SonneS2_Tiefe18']*mean_ratio_s2

 
#mehrere plots erstellen
#Sonnenstation
fig, ax5 = plt.subplots(figsize=(12,6))
ax5.plot(df_pivot["time"], df_pivot['Sonnenstation_1'], label="SO", color="orange")
ax5.plot(df_pivot["time"], df_pivot['Sonnenstation_2'], label="SU", color="blue")
ax5.plot(df_pivot["time"], df_pivot['SonneS2_Tiefe18'], label="SU 0,18m Tiefe", linestyle="--")
ax5.set_ylabel("Strahlung (W/m²)")
ax5.set_xlabel("Zeit (MESZ)")
#ax5.set_title("Tagesverlauf der Strahlungswerte der Sonnenstation über Wasser, 0,31m tief und 0,18m tief")
ax5.legend()
ax5.grid(True)
ax5.set_xlim(pd.Timestamp("2025-08-10 00:00"),
             pd.Timestamp("2025-08-11 00:00"))
ax5.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax5.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M"))
ax5.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0,15,30,45]))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()

#Dunkelstationen
fig, ax6 = plt.subplots(figsize=(12,6))
ax6.plot(df_pivot["time"], df_pivot['Dunkelstation_1'], label="DO", color="orange")
ax6.plot(df_pivot["time"], df_pivot['Dunkelstation_2'], label="DU", color="blue")
ax6.plot(df_pivot["time"], df_pivot['Dunkelstation_1_Neu'], label="DO berechnet", color="green", linestyle="--")
ax6.plot(df_pivot["time"], df_pivot['Dunkelstation_2_Neu'], label="DU berechnet", color="purple", linestyle="--")
ax6.set_ylabel("Strahlung (W/m²)")
ax6.set_xlabel("Zeit (MESZ)")
#ax6.set_title("Tagesverlauf der Strahlungswerte der Dunkelstation roh(mitNaN) und berechnet")
ax6.legend()
ax6.grid(True)
ax6.set_xlim(pd.Timestamp("2025-08-10 00:00"),
             pd.Timestamp("2025-08-11 00:00"))
ax6.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax6.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m. %H:%M"))
ax6.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0,15,30,45]))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()

#d1neu d2neu s1 s2neu
fig, ax3 = plt.subplots(figsize=(12,6))
ax3.plot(df_pivot["time"], df_pivot['Sonnenstation_1'], label="SO", color="orange")
ax3.plot(df_pivot["time"], df_pivot['SonneS2_Tiefe18'], label="SU 0,18m tief", color="blue")
ax3.plot(df_pivot["time"], df_pivot['Dunkelstation_1_Neu'], label="DO berechnet", color="green")
ax3.plot(df_pivot["time"], df_pivot['Dunkelstation_2_Neu'], label="DU berechnet", color="purple")
ax3.set_ylabel("Strahlung (W/m²)")
ax3.set_xlabel("Zeit (MESZ)")
#ax3.set_title("Tagesverlauf der Strahlungswerte der Dunkel- und Sonnnenstation aufbereitet")
ax3.legend()
ax3.grid(True)
ax3.set_xlim(pd.Timestamp("2025-08-10 00:00"),
             pd.Timestamp("2025-08-11 00:00"))
ax3.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M"))
ax3.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0,15,30,45]))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()

#Verhältnisse
fig, ax4 = plt.subplots(figsize=(12,6))
ax4.plot(df_pivot["time"], df_pivot['ratio_s1'], label="D1/S1 ")
ax4.plot(df_pivot["time"], df_pivot['ratio_s2'], label="D2/S2 Neu")
ax4.set_ylabel("Verhältnis Dunkel/Sonne")
ax4.set_ylim(0.0, 0.8)
#ax4.set_title("Verhältnisse")
ax4.legend()
ax4.grid(True)
ax4.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M"))
ax4.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0,15,30,45]))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()