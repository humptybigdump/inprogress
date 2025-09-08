# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 11:42:47 2025

@author: mai-w

Vergleich Messung vs. Kosinus-Modell:
- Rohdaten und stündlich gemittelte Daten
- Skalierung des Kosinus-Modells auf Messung
- Berechnung des Korrelationskoeffizienten
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# ---------------- Einstellungen ----------------
CSV_PATH   = "sonnenstation_korrigiert_1min.csv"   # Pfad zur Messdatei
DATE_STR   = "2025-08-10"                          # Datum für Analyse
sunrise_h  = 6.0                                   # angenommene Sonnenaufgangszeit (h)
sunset_h   = 21.0                                  # angenommene Sonnenuntergangszeit (h)
I0         = 1000.0                                # Maximalwert der Modellstrahlung (W/m²)
MEASURE_COLS_TRY = ["S1_original", "S2_original"]  # mögliche Messspalten

# ---------------- Hilfsfunktionen ----------------
def cos_theory(t_hours, sunrise=6.0, sunset=21.0, I0=1000.0):
    """
    Berechnet den theoretischen Kosinus-Verlauf zwischen sunrise und sunset.
    t_hours: Zeit in Stunden (float oder array)
    """
    theta = (t_hours - sunrise) / (sunset - sunrise) * np.pi
    curve = np.where((t_hours >= sunrise) & (t_hours <= sunset),
                     np.cos(theta - np.pi/2),  # Kosinusbogen zwischen 0 und π
                     0.0)                      # außerhalb: 0
    return I0 * curve

def fit_scale(y_meas, y_theo):
    """
    Findet Skalierungsfaktor, um Theorie an Messwerte anzupassen
    (Least-Squares Fit ohne Offset).
    """
    y_meas = np.asarray(y_meas, dtype=float)
    y_theo = np.asarray(y_theo, dtype=float)
    valid  = (~np.isnan(y_meas)) & (y_theo > 0)   # nur gültige Messungen berücksichtigen
    if np.any(valid):
        return float(np.sum(y_meas[valid] * y_theo[valid]) / np.sum(y_theo[valid]**2))
    return 1.0

def pearson_r(a, b):
    """
    Berechnet Pearson-Korrelation zwischen zwei Arrays.
    Gibt (r, p) zurück, oder (nan, nan) wenn zu wenig Datenpunkte.
    """
    mask = (~np.isnan(a)) & (~np.isnan(b))
    if mask.sum() < 3:
        return np.nan, np.nan
    return pearsonr(a[mask], b[mask])

# ---------------- Daten laden ----------------
df = pd.read_csv(CSV_PATH)

# Zeitstempel als datetime interpretieren
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Zeitzone sicherstellen → Europe/Berlin
df["timestamp"] = (df["timestamp"].dt.tz_localize("Europe/Berlin")
                   if df["timestamp"].dt.tz is None
                   else df["timestamp"].dt.tz_convert("Europe/Berlin"))

# Tagesgrenzen für gewünschtes Datum bestimmen
day_start = pd.Timestamp(DATE_STR).tz_localize("Europe/Berlin")
day_end   = day_start + pd.Timedelta(days=1)

# Nur Daten dieses Tages auswählen
day = df[(df["timestamp"] >= day_start) & (df["timestamp"] < day_end)].copy()

# Messspalte bestimmen (erste, die existiert)
measured_col = next((c for c in MEASURE_COLS_TRY if c in day.columns), None)

# Zeit in Stunden (für Modell)
day["t_hours"] = (day["timestamp"].dt.hour
                  + day["timestamp"].dt.minute/60
                  + day["timestamp"].dt.second/3600)

# ---------------- Rohdaten ----------------
t_raw = day["t_hours"].to_numpy()
y_raw = day[measured_col].astype(float).to_numpy()

# Theorie-Kurve + Skalierung
y_theo_raw = cos_theory(t_raw, sunrise_h, sunset_h, I0)
scale_raw  = fit_scale(y_raw, y_theo_raw)
y_theo_raw *= scale_raw

# Korrelation
r_raw, p_raw = pearson_r(y_raw, y_theo_raw)

# ---------------- Stündlich gemittelt ----------------
day_idx = day.set_index("timestamp")
hourly = day_idx[measured_col].resample("1H").mean().to_frame("meas")
hourly["t_hours"] = hourly.index.hour + hourly.index.minute/60

t_hour = hourly["t_hours"].to_numpy()
y_hour = hourly["meas"].to_numpy(dtype=float)

# Theorie-Kurve + Skalierung
y_theo_hour = cos_theory(t_hour, sunrise_h, sunset_h, I0)
scale_hour  = fit_scale(y_hour, y_theo_hour)
y_theo_hour *= scale_hour

# Korrelation
r_hour, p_hour = pearson_r(y_hour, y_theo_hour)

# ---------------- Plot ----------------
fig, axes = plt.subplots(1, 2, figsize=(12,5), sharey=True)

# (a) stündlich gemittelt
ax = axes[0]
ax.plot(t_hour, y_theo_hour, lw=2, label="Theorie (Kosinus)")
ax.plot(t_hour, y_hour, "o-", alpha=0.9, label="Messung stündlich")
ax.axvline(sunrise_h, ls="--", alpha=0.6)
ax.axvline(sunset_h,  ls="--", alpha=0.6)
ax.set_xlim(0,24)
ax.set_xlabel(" Uhrzeit in Stunden (MESZ)")
ax.set_ylabel("Strahlung [W/m²]")
ax.set_title("(a) Stündlich gemittelt")
ax.legend(loc="upper left")
# Korrelation unter Legende
ax.text(0.02, 0.80, f"r = {r_hour:.2f}", transform=ax.transAxes,
        ha="left", va="top")

# (b) Rohdaten
ax = axes[1]
ax.plot(t_raw, y_theo_raw, lw=2, label="Theorie (Kosinus)")
ax.plot(t_raw, y_raw, alpha=0.8, label="Messung roh")
ax.axvline(sunrise_h, ls="--", alpha=0.6)
ax.axvline(sunset_h,  ls="--", alpha=0.6)
ax.set_xlim(0,24)
ax.set_xlabel("Uhrzeit in Stunden (MESZ)")
ax.set_title("(b) Nicht gemittelt")
ax.legend(loc="upper left")
ax.text(0.02, 0.80, f"r = {r_raw:.2f}", transform=ax.transAxes,
        ha="left", va="top")

# Gesamttitel
#fig.suptitle(f"Vergleich Messung vs. Kosinus-Modell (6–21 Uhr) am {DATE_STR}", y=1.02)
plt.tight_layout()
plt.show()
