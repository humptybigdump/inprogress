# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 10:45:53 2025

@author: lenny
"""

import pandas as pd
import numpy as np
from scipy.interpolate import PchipInterpolator

# --- CSV-Dateien einlesen ---
csv1 = "mobile_messung_aufbereitet.csv"
csv2 = "sonnenstation_korrigiert_10min.csv"

df1 = pd.read_csv(csv1)
df2 = pd.read_csv(csv2)

# --- Zeiten in datetime umwandeln ---
df1["time"] = pd.to_datetime(df1["time"], utc=True)
df2["timestamp"] = pd.to_datetime(df2["timestamp"], utc=True)

# --- MESZ konvertieren ---
df1["time_mesz"] = df1["time"].dt.tz_convert("Europe/Berlin")
df2["time_mesz"] = df2["timestamp"].dt.tz_convert("Europe/Berlin")

# --- auf 10 Minuten abrunden (immer zur unteren Grenze) ---
df1["time_10min"] = df1["time_mesz"].dt.floor("10min")
df2["time_10min"] = df2["time_mesz"].dt.floor("10min")

# --- Spalten umbenennen mit Präfix ---
df1 = df1.rename(columns={
    "time": "csv1_time",
    "strahlung_korr": "csv1_strahlung_korr",
    "time_mesz": "csv1_time_mesz",
    "time_10min": "csv1_time_10min"
})
df2 = df2.rename(columns={
    "timestamp": "csv2_timestamp",
    "S1_plot_blended": "csv2_sensor2",
    "time_mesz": "csv2_time_mesz",
    "time_10min": "csv2_time_10min"
})

# --- DataFrames zusammenführen (auf 10min gerundet) ---
df_merged = pd.merge(
    df1,
    df2[["csv2_time_10min", "csv2_sensor2"]],
    left_on="csv1_time_10min",
    right_on="csv2_time_10min",
    how="left"
)

# --- Verhältnis-Spalte ---
df_merged["strahlungs_verhaeltnis"] = (
    df_merged["csv1_strahlung_korr"] / df_merged["csv2_sensor2"]
)

# --- df_merged nach fluss_idx und Zeit gruppieren und Mittelwert bilden ---
df_merged_avg = df_merged.groupby(
    ["fluss_idx", "csv1_time_10min"], as_index=False
)["strahlungs_verhaeltnis"].mean()


# --- Tages-Matrix für Tagesgang erstellen ---

# Uhrzeit (nur Stunden:Minuten) extrahieren
df_merged_avg["time_only"] = df_merged_avg["csv1_time_10min"].dt.time

# Gruppieren nach fluss_idx und Uhrzeit, Mittelwert berechnen
df_day_avg = (
    df_merged_avg
    .groupby(["fluss_idx", "time_only"], as_index=False)["strahlungs_verhaeltnis"]
    .mean()
)

# Pivot-Tabelle: Zeilen = Uhrzeit, Spalten = Segmente
day_matrix = df_day_avg.pivot(
    index="time_only",
    columns="fluss_idx",
    values="strahlungs_verhaeltnis"
)

# --- Sicherstellen, dass alle 10-Minuten-Schritte enthalten sind ---
# vollständige Uhrzeitliste von 00:00 bis 23:50 im 10-Minuten-Raster
import datetime as dt
full_times = [ (dt.datetime(2000,1,1,0,0) + dt.timedelta(minutes=10*i)).time()
               for i in range(24*6) ]  # 144 Werte

# Index auf vollständiges Raster setzen (fehlende Werte = NaN)
day_matrix = day_matrix.reindex(full_times)

# Index ggf. in Strings ("HH:MM") umwandeln für bessere Lesbarkeit/Export
day_matrix.index = [t.strftime("%H:%M") for t in day_matrix.index]

# Optional: Index zurück in Spalte für CSV
day_matrix_reset = day_matrix.reset_index().rename(columns={"index": "time"})

# Ergebnis speichern
day_matrix_reset.to_csv("strahlungs_tagesmatrix.csv", index=False)


# ----Interpolation------

# --- Index in datetime.time konvertieren, falls Strings ---
if day_matrix.index.dtype == object or isinstance(day_matrix.index[0], str):
    day_matrix.index = pd.to_datetime(day_matrix.index, format="%H:%M").time

# --- Interpolation vorbereiten ---
day_matrix_interp = day_matrix.copy()

# Index in Minuten (von 00:00 bis 23:50)
time_minutes = np.array([t.hour*60 + t.minute for t in day_matrix.index])

# 00:00 und 23:50 auf 1 setzen
day_matrix_interp.iloc[0, :] = 1      # 00:00
day_matrix_interp.iloc[-1, :] = 1     # 23:50

# Interpolation
for col in day_matrix.columns:
    y = day_matrix_interp[col].values.astype(float)
    mask = ~np.isnan(y)
    if mask.sum() > 1:
        f = PchipInterpolator(time_minutes[mask], y[mask])
        day_matrix_interp[col] = f(time_minutes)
        
# Werte > 1 auf 1 setzen
before_clip = (day_matrix_interp > 1).sum().sum()  # Anzahl Werte > 1 vor Clipping

day_matrix_interp = day_matrix_interp.clip(upper=1)

after_clip = (day_matrix_interp >= 1).sum().sum()  # Anzahl Werte == 1 nach Clipping

print(f"Es wurden {before_clip} Werte auf 1 geclippt.")
print(f"Kontrolle: Es gibt jetzt {after_clip} Werte == 1.")


# Größter und kleinster Wert in der interpolierten Tagesmatrix
print("Min Wert:", day_matrix_interp.min().min())
print("Max Wert:", day_matrix_interp.max().max())

# Anzahl Tage
n_days = 14

# Tagesmatrix 14 Mal untereinander stapeln
full_ratio_matrix = pd.concat([day_matrix_interp]*n_days, ignore_index=True)

# Optional: Index als Datetime von 04.08.2025 00:00 bis 17.08.2025 23:50 setzen
start_date = pd.Timestamp("2025-08-04 00:00", tz="Europe/Berlin")
time_index = pd.date_range(
    start=start_date,
    periods=full_ratio_matrix.shape[0],
    freq="10min",
    tz="Europe/Berlin"
)
full_ratio_matrix.index = time_index

# Ergebnis speichern
full_ratio_matrix_reset = full_ratio_matrix.reset_index().rename(columns={"index": "time"})
full_ratio_matrix_reset.to_csv("strahlungs_14tage_ratio.csv", index=False)

print("Matrix für 14 Tage erstellt:", full_ratio_matrix_reset.shape)

# ----Strahlungsmatrix berechnen------------
# df2: csv2_sensor2 Werte, auf 10-Minuten-Zeitschritte gerundet
# full_ratio_matrix: bereits 14 Tage × 453 Segmente, index = Zeit (DatetimeIndex)

# 1. csv2_sensor2 auf den Index der Matrix ausrichten
# Reindex mit Forward-Fill oder NaN, je nach Bedarf
df2_reindexed = df2.set_index("csv2_time_10min").reindex(full_ratio_matrix.index, method="ffill")

# 2. Extrahiere die Strahlung als Array
strahlung = df2_reindexed["csv2_sensor2"].values  # Länge = 2016

# 3. Komponentenweise multiplizieren
strahlung_matrix = full_ratio_matrix.values * strahlung[:, np.newaxis]  # broadcasting

# 4. Optional: zurück in DataFrame, Werte auf ganze Zahlen floored
# Negative Werte auf 0 setzen, NaNs auf 0 setzen, dann floor und int
strahlung_matrix_clean = np.nan_to_num(strahlung_matrix, nan=0.0)  # NaNs → 0.0
strahlung_matrix_int = np.floor(np.maximum(strahlung_matrix_clean, 0)).astype(int)

strahlung_matrix_df = pd.DataFrame(
    strahlung_matrix_int,
    index=full_ratio_matrix.index,
    columns=full_ratio_matrix.columns
)

# 5. CSV speichern
strahlung_matrix_df_reset = strahlung_matrix_df.reset_index().rename(columns={"index": "time"})
strahlung_matrix_df_reset.to_csv("strahlung_14tage_abs.csv", index=False)

print("Ergebnismatrix erstellt:", strahlung_matrix_df_reset.shape)

# Größter und kleinster Wert in der interpolierten Tagesmatrix
print("Min Wert:", strahlung_matrix_df.min().min())
print("Max Wert:", strahlung_matrix_df.max().max())




