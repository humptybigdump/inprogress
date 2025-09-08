#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 17:03:37 2025

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
df_plot_Wochenverlauf= df_prepared[df_prepared["sensor"].isin(sensoren)].copy()

#filtern sodass nur der eine Tag im df ist (zeitsparend)
start_day = "2025-08-04 00:00:00"
end_day = "2025-08-17 23:59:59"
df_plot_Wochenverlauf = df_plot_Wochenverlauf[(df_plot_Wochenverlauf["time"] >= start_day) & (df_plot_Wochenverlauf["time"] <= end_day)]

# === Zeitbasierte Glättung (30 Minuten) ===
df_plot_Wochenverlauf = df_plot_Wochenverlauf.copy()

# Index auf Zeit setzen, damit rolling("30min") funktioniert
df_plot_Wochenverlauf = df_plot_Wochenverlauf.set_index("time")

#alles glätten
df_plot_Wochenverlauf["value_smooth"] = (
    df_plot_Wochenverlauf.groupby("sensor")["value"]
    .transform(lambda x: x.rolling("10min", min_periods=1).mean())
) 

# Original-NaNs auch in value_smooth übernehmen
df_plot_Wochenverlauf.loc[df_plot_Wochenverlauf["value"].isna(), "value_smooth"] = float("nan")

# Zeit zurück als normale Spalte (praktisch für Plotten)
df_plot_Wochenverlauf = df_plot_Wochenverlauf.reset_index()

sensor1highlights = [
    ("07:35", "08:35"),
    ("09:30", "11:25"),
    ("15:50", "18:25")
]
sensor2highlights = [
    ("09:40", "11:40"),
    ("15:45", "18:20")
]

cut = {
    "Dunkelstation_1": sensor1highlights,
    "Dunkelstation_2": sensor2highlights
}

# Alle Tage aus df extrahieren
tage = df_plot_Wochenverlauf['time'].dt.date.unique()
for sensor, intervals in cut.items():
    for start_str, end_str in intervals:
        for tage_i in tage:  # einzelnes Datum aus der Liste
            start = datetime.combine(tage_i, datetime.strptime(start_str, "%H:%M").time())
            end   = datetime.combine(tage_i, datetime.strptime(end_str, "%H:%M").time())
            
            mask = (df_plot_Wochenverlauf['sensor'] == sensor) & (df_plot_Wochenverlauf['time'] >= start) & (df_plot_Wochenverlauf['time'] <= end)
            df_plot_Wochenverlauf.loc[mask, 'value_smooth'] = float('nan')
   
# --- 1-Minuten-Raster je Sensor (mean) mit komplettem Tagesindex ---
full_min_idx = pd.date_range(start=start_day, end=end_day, freq="1min")

dfs = []
for sensor, g in df_plot_Wochenverlauf.groupby("sensor"):
    # auf Minuten mitteln
    gm = (g.set_index("time")
            .resample("1min")["value_smooth"]
            .mean()
            .reindex(full_min_idx))  # Lücken auf vollständigen Minutenraster ausdehnen (NaN)
    gm = gm.rename_axis("time").to_frame("value_smooth")
    gm["sensor"] = sensor
    dfs.append(gm.reset_index())

df_plot_Wochenverlauf = pd.concat(dfs, ignore_index=True)

# --- Pivot aus der 1-Minuten-Serie aufbauen ---
df_pivot = df_plot_Wochenverlauf.pivot(index="time", columns="sensor", values="value_smooth")

# --- k zunächst roh berechnen (tagsüber + nachts) ---
k_raw = -(np.log(df_pivot["Sonnenstation_2"] / df_pivot["Sonnenstation_1"])) / 0.31

#Sonnenaufgang und untergang je nach Tag
braeunungszeit = {
    "2025-08-04": ("06:01", "20:59"),
    "2025-08-05": ("06:02", "20:57"),
    "2025-08-06": ("06:03", "20:56"),
    "2025-08-07": ("06:05", "20:54"),
    "2025-08-08": ("06:06", "20:52"),
    "2025-08-09": ("06:07", "20:51"),
    "2025-08-10": ("06:09", "20:49"),
    "2025-08-11": ("06:10", "20:48"),
    "2025-08-12": ("06:12", "20:46"),
    "2025-08-13": ("06:13", "20:44"),
    "2025-08-14": ("06:14", "20:42"),
    "2025-08-15": ("06:16", "20:41"),
    "2025-08-16": ("06:17", "20:39"),
    "2025-08-17": ("06:18", "20:37")
}

# 2. Funktion, die für einen Timestamp prüft, ob es Nacht ist
def is_night(ts):
    tag_str = ts.date().isoformat()  # z.B. "2025-08-10"
    sunrise_str, sunset_str = braeunungszeit[tag_str]
    sunrise = datetime.combine(ts.date(), datetime.strptime(sunrise_str, "%H:%M").time())
    sunset  = datetime.combine(ts.date(), datetime.strptime(sunset_str, "%H:%M").time())
    
    return (ts >= sunset) or (ts <= sunrise)

# 3. Maske anwenden
night_mask = df_pivot.index.map(is_night)
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

# 3. Maske anwenden
df_pivot["ratio_s1"] = df_pivot["ratio_s1"].mask(night_mask)
df_pivot["ratio_s2"] = df_pivot["ratio_s2"].mask(night_mask)

#Datum extrahieren
df_pivot['date'] = df_pivot['time'].dt.date

# Mittelwerte pro Tag berechnen
taeglich_mittelwerte = df_pivot.groupby('date')[['ratio_s1', 'ratio_s2']].mean()

# Ausgabe
print("📈 Tägliche Mittelwerte der Verhältnisse:")
for date, row in taeglich_mittelwerte.iterrows():
    print(f"   {date} -> S1 = {row['ratio_s1']:.3f}, S2 = {row['ratio_s2']:.3f}")

df_pivot = df_pivot.merge(taeglich_mittelwerte, on='date', how='left', suffixes=('', '_tag'))
df_pivot['Dunkelstation_1_Neu'] = df_pivot['Sonnenstation_1'] * df_pivot['ratio_s1_tag']
df_pivot['Dunkelstation_2_Neu'] = df_pivot['SonneS2_Tiefe18'] * df_pivot['ratio_s2_tag']

df_pivot.loc[night_mask, 'Dunkelstation_2_Neu'] = 0
df_pivot.to_csv("dunkelstation_korrigiert_1min.csv", index=False, sep=";")


#mehrere plots erstellen
#Sonnenstation
fig, ax1 = plt.subplots(figsize=(12,6))
ax1.plot(df_pivot["time"], df_pivot['Sonnenstation_1'], label="S1")
ax1.plot(df_pivot["time"], df_pivot['Sonnenstation_2'], label="S2")
ax1.plot(df_pivot["time"], df_pivot['SonneS2_Tiefe18'], label="S2 Neu", linestyle="--")
ax1.set_ylabel("Strahlung (W/m²)")
ax1.set_title("2-Wochenverlauf Sonnenstation")
ax1.legend()
ax1.grid(True)
ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m. %H:%M'))
ax1.set_xlim(pd.Timestamp("2025-08-04 00:00"),
             pd.Timestamp("2025-08-17 23:59"))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()

#Dunkelstationen
fig, ax2 = plt.subplots(figsize=(12,6))
ax2.plot(df_pivot["time"], df_pivot['Dunkelstation_1'], label="D1")
ax2.plot(df_pivot["time"], df_pivot['Dunkelstation_2'], label="D2")
ax2.plot(df_pivot["time"], df_pivot['Dunkelstation_1_Neu'], label="D1 Neu", linestyle="--")
ax2.plot(df_pivot["time"], df_pivot['Dunkelstation_2_Neu'], label="D2 Neu", linestyle="--")
ax2.set_ylabel("Strahlung (W/m²)")
ax2.set_title("2-Wochenverlauf Dunkelstation")
ax2.legend()
ax2.grid(True)
ax2.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m. %H:%M'))
ax2.set_xlim(pd.Timestamp("2025-08-04 00:00"),
             pd.Timestamp("2025-08-17 23:59"))
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
ax3.set_xlabel("Strahlung (W/m²)")
#ax3.set_title("Strahlungswerte Dunkelstation und Sonnenstation neu")
ax3.legend()
ax3.grid(True)
ax3.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m. %H:%M'))
ax3.set_xlim(pd.Timestamp("2025-08-04 00:00"),
             pd.Timestamp("2025-08-17 23:59"))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()

#Verhältnisse
fig, ax4 = plt.subplots(figsize=(12,6))
ax4.plot(df_pivot["time"], df_pivot['ratio_s1'], label="D1/S1 ")
ax4.plot(df_pivot["time"], df_pivot['ratio_s2'], label="D2/S2 Neu")
ax4.set_ylabel("Verhältnis Dunkel/Sonne")
ax4.set_ylim(0.0, 0.8)
ax4.set_title("Verhältnisse")
ax4.legend()
ax4.grid(True)
ax4.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m. %H:%M'))
ax4.set_xlim(pd.Timestamp("2025-08-04 00:00"),
             pd.Timestamp("2025-08-17 23:59"))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()

