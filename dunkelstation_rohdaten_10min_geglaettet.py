#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 14:31:40 2025

@author: jule
"""

from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# === CSV-Datei einlesen===================================================================
# Pfad zur CSV-Datei
csvfile = "dunkelstation_roh.csv"
# CSV einlesen
# Falls deine Datei Semikolons statt Kommas als Trennzeichen hat, sep=";" verwenden
df_raw = pd.read_csv(csvfile, sep=",")  

# Führende und abschließende Leerzeichen aus allen Spaltennamen entfernen
df_raw.columns = df_raw.columns.str.strip()

# Zeitstempel in datetime umwandeln(welche Zeit man weis es nicht)
df_raw["Zeitstempel"] = pd.to_datetime(df_raw["Zeitstempel"])


# === In Langformat bringen: time, sensor, value ===
data = []

for _, row in df_raw.iterrows():
    ts = row["Zeitstempel"]
    data.append((ts, "Dunkelstation_1", row["Strahlung_S1mittel"]))
    data.append((ts, "Dunkelstation_2", row["Strahlung_S2mittel"]))

# === DataFrame erstellen ===
df = pd.DataFrame(data, columns=["time", "sensor", "value"])

# === DataFrame erstellen ===
df = pd.DataFrame(data, columns=["time", "sensor", "value"])

# === Sortieren (wichtig!) ===
df.sort_values(["sensor", "time"], inplace=True)

# === Datenlücken > 5 min mit NaN markieren ===
max_gap = timedelta(minutes=5)

# Neues DataFrame für geplottete Daten
df_prepared = pd.DataFrame(columns=["time", "sensor", "value"])

for sensor_name, group in df.groupby("sensor"):
    group = group.reset_index(drop=True)
    new_rows = [group.iloc[0].to_dict()]

    for i in range(1, len(group)):
        time_diff = group.loc[i, "time"] - group.loc[i - 1, "time"]
        if time_diff > max_gap:
            # NaN-Zeile einfügen um die Linie zu unterbrechen
            new_rows.append({"time": group.loc[i - 1, "time"] + max_gap/2,
                             "sensor": sensor_name, "value": float('nan')})
        new_rows.append(group.iloc[i].to_dict())

    df_prepared = pd.concat([df_prepared, pd.DataFrame(new_rows)], ignore_index=True)
    
print(f"📊 Ursprüngliche Daten: {len(df)} Zeilen")
print(f"📊 Mit NaN-Lücken:      {len(df_prepared)} Zeilen")

# === Filter für Dunkelstation Sensor 1 und 2 ===
dunkelsensoren = ["Dunkelstation_1", "Dunkelstation_2"]
df_plot_dunkelstation = df_prepared[df_prepared["sensor"].isin(dunkelsensoren)]

# === Zeitbasierte Glättung (30 Minuten) ===
df_plot_dunkelstation = df_plot_dunkelstation.copy()

# Index auf Zeit setzen, damit rolling("30min") funktioniert
df_plot_dunkelstation = df_plot_dunkelstation.set_index("time")

df_plot_dunkelstation["value_smooth"] = (
    df_plot_dunkelstation.groupby("sensor")["value"]
    .transform(lambda x: x.rolling("10min", min_periods=1).mean())
)


# Original-NaNs auch in value_smooth übernehmen
df_plot_dunkelstation.loc[df_plot_dunkelstation["value"].isna(), "value_smooth"] = float("nan")

df_plot_dunkelstation = df_plot_dunkelstation.reset_index()

end_time = pd.Timestamp("2025-08-17 23:59")
start_time = pd.Timestamp("2025-08-04 00:00:00")
df_plot_dunkelstation = df_plot_dunkelstation[(df_plot_dunkelstation["time"] >= start_time) & (df_plot_dunkelstation["time"] <= end_time)]



df_pivot = df_plot_dunkelstation.pivot(index="time", columns="sensor", values="value_smooth")
df_plot_dunkelstation= df_pivot
df_plot_dunkelstation = df_plot_dunkelstation.reset_index()
# === Plot erstellen ===
fig, ax1 = plt.subplots(figsize=(12,6))
ax1.plot(df_plot_dunkelstation["time"], df_plot_dunkelstation['Dunkelstation_1'], label="DO", color="tab:orange")
ax1.plot(df_plot_dunkelstation["time"], df_plot_dunkelstation['Dunkelstation_2'], label="DU", color="tab:blue")

plt.ylabel("Strahlung (W/m²)")
plt.xlabel("Zeit (MESZ)")
#plt.title("Strahlungswerte der Dunkelstation - 10 Minuten geglättet")
plt.legend()
plt.grid(True)
ax1.grid(True)
ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=[12]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m. %H:%M'))
ax1.set_xlim(pd.Timestamp("2025-08-04 00:00"),
             pd.Timestamp("2025-08-17 23:59"))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()
plt.show()
