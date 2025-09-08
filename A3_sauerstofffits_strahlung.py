# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 09:18:47 2025

@author: Elisa Nawrot, Lara Wadlinger, Benedikt Döllmann
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp
import pandas as pd
import matplotlib.dates as mdates
from datetime import timedelta

#%% Anmerkung: Wir haben bemerkt, dass je nach dem welchen Laptop, also je nach Python-Installation, wir verwendet haben 
# teilweise unterschiedliche Fits und Parameter enstanden, obwohl genau der selbe Code verwendet wurde.
# Wir wissen nicht woran das liegt. Die Parameter die im Bericht zu finden sind und für die Auswertung verwendet wurden,
# stammen von Lara Wadlingers Laptop.
#%% Funktionen
# Einlese-Funktion der Sauerstoff-Daten
def read(filepath):
    # CSV-Dateien einlesen
    df = pd.read_csv(filepath, sep=",", skiprows=2)
    # Überflüssigen Leerzeichen in Spaltennamen entfernen
    df.columns = [col.strip() for col in df.columns]
    # Nur die relevanten Spalten zurückgeben
    return df[['Time (sec)', 'DO (mg/l)']]


# Funktion für den linearen Fotosynthese-Fit
def fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0):
    # Differentialgleichung des linearen Gesetzes
    def dcdt(t, DO, k_photo, r_zehr_max, K_M, rad_times_full, rad_values_full):
        R_eff = np.interp(t, rad_times_full, rad_values_full)  # Strahlung zur Zeit t interpolieren
        r_zehr = (r_zehr_max * DO) / (K_M + DO)                # Zehrung nach Michaelis-Menten
        return k_photo * R_eff - r_zehr                        

    # Sauerstoffmodell: Lösung der DGL mit solve_ivp
    def do_model(t_eval, DO0, k_photo, r_zehr_max, K_M):
        sol = solve_ivp(
            fun=lambda t, DO: dcdt(t, DO, k_photo, r_zehr_max, K_M, rad_times_full, rad_values_full),
            t_span=(t_eval[0], t_eval[-1]),  # Integrationsbereich
            y0=[DO0],                        # Startwert für DO
            t_eval=t_eval                    # Zeitpunkte zur Berechnung festlegen
            )
        return sol.y[0]  # liefert c(t) zurück

    # Root-Mean-Square-Error (RMSE) zur Bewertung der Anpassungsgüte
    def rmse(c_meas, c_sim):
        return np.sqrt(np.mean((c_meas - c_sim) ** 2))

    # Modell an die Messdaten anpassen
    # p0 = Startwerte für die Parameter [DO0, k_photo, r_zehr_max, K_M]
    params, cov = curve_fit(do_model, t_data, y_data, p0=p0)

    # Simulation mit den gefitteten Parametern
    y_sim = do_model(t_data, *params)

    # RMSE berechnen
    rmse_val = rmse(y_data, y_sim)

    # Unsicherheiten der Parameter (Standardabweichung aus Kovarianzmatrix)
    perr = np.sqrt(np.diag(cov))  

    # Ergebnisse zurückgeben
    return {
        "params": params,  # Parameterwerte
        "cov": cov,        # Kovarianzmatrix
        "perr": perr,      # Unsicherheiten
        "rmse": rmse_val,  # Anpassungsgüte
        "y_sim": y_sim     # simulierte Zeitreihe
    }

# Funktion für den Michaelis-Menten Modellfit
def fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0):
    # Differentialgleichung mit Michaelis-Menten-Photosynthese
    def dcdt(t, DO, r_photo_max, R_05, r_zehr_max, K_M, rad_times_full, rad_values_full):
        R_eff = np.interp(t, rad_times_full, rad_values_full)     # Strahlung zur Zeit t interpolieren
        r_zehr = (r_zehr_max * DO) / (K_M + DO)                  # Zehrung nach Michaelis-Menten
        r_photo = ((r_photo_max * R_eff) / (R_eff + R_05)) - r_zehr  
        return r_photo
    
    # Sauerstoffmodell: Lösung der DGL mit solve_ivp
    def do_model_mm(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
        sol = solve_ivp(
            fun=lambda t, DO: dcdt(t, DO, r_photo_max, R_05, r_zehr_max, K_M, rad_times_full, rad_values_full),
            t_span=(t_eval[0], t_eval[-1]),  # Integrationsbereich
            y0=[DO0],                        # Startwert für DO
            t_eval=t_eval                    # Auswertezeitpunkte
        )
        return sol.y[0] #liefert c(t) zurück

    # Root-Mean-Square-Error (RMSE) zur Bewertung der Anpassungsgüte
    def rmse(c_meas, c_sim):
        return np.sqrt(np.mean((c_meas - c_sim) ** 2))

     # Modell an die Messdaten anpassen
    params, cov = curve_fit(do_model_mm, t_data, y_data, p0=p0)

    # Simulation mit den gefundenen Parametern
    # p0 = Startwerte für die Parameter [DO0, r_photo_max, R_05, r_zehr_max, K_M]
    y_sim = do_model_mm(t_data, *params)

    # RMSE berechnen
    rmse_val = rmse(y_data, y_sim)

    # Unsicherheiten der Parameter (Standardabweichung aus Kovarianzmatrix)
    perr = np.sqrt(np.diag(cov))

    # Ergebnisse zurückgeben
    return {
        "params": params,
        "cov": cov,
        "perr": perr,
        "rmse": rmse_val,
        "y_sim": y_sim
    }
#%% Messung: Sonnenbox vom 5.-6.8.2025
#Sauerstoffdaten einlesen
df1 = read("Messung2Sonne.txt")
df2 = read("Messung2.2Sonne.txt")

#Zusammenfügen & Zeitstempel anpassen
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0] # Berechne Zeit relativ zur ersten Messung
start_datetime = pd.Timestamp("2025-08-05 14:38:00") # Startzeitpunkt
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Kürzen der Daten über die Zeit
start_time = df['Time'].iloc[0] + timedelta(minutes=390)
end_time = df['Time'].iloc[-1] - timedelta(minutes=200)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: hier Verwendung der Strahlungsdaten aus der Box
df_rad = pd.read_csv("merged_Dunkel_S2__Pflanze_S1.txt", parse_dates=["timestamp_europe_berlin"])
df_rad = df_rad.rename(columns={"timestamp_europe_berlin": "time", "pflanzenstation_sensor1_w_m2": "Radiation", "dunkelstation_sensor2_w_m2": "Radiation1"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit Strahlung verwenden; keine NaN Werte
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten zeitlich zu Sauerstoffdaten anpassen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

# Sauerstoffdaten für den Modellfit definieren
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
y_data = df_filtered['DO (mg/l)'].values

# Strahlungsdaten für den Modellfit definieren
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values

# Fit-Berechnungen
# Lineares Modell
p0_linear = [y_data[0], 1e-6, 1e-3, 1e-4] # Startwerte

# Michaelis-Menten Modell
p0_mm = [y_data[0], 1e-3, 1e2, 1e-1, 1e-5] #Startwerte

#Modellfit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

#Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M')) #Datum und Uhrzeit-Formatierung

# Plotten der Fits
# Erzeugung gleichmäßig verteilter Zeitpunkte, auf denen das Modell ausgewertet wird
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
# Umwandlung der Zeitpunkte von Sekunden in einen Zeitstempel 
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Linearer Fit: herausziehen zum Plotten
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Fit: herausziehen zum Plotten
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) / 
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=18)

plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()

#%% Messung: Sonnenbox vom 6.-7.8.2025
# Sauerstoffdaten einlesen
df1 = read("Messung3Sonne.txt")
df2 = read("Messung3.2Sonne.txt")

# Zusammenfügen & Zeitstempel anpassen
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]   # Zeit relativ zur ersten Messung
start_datetime = pd.Timestamp("2025-08-06 15:10:00")                # Startzeitpunkt der Messung
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Kürzen der Daten auf einen relevanten Zeitraum
start_time = df['Time'].iloc[0] + timedelta(minutes=400)
end_time = df['Time'].iloc[-1] - timedelta(minutes=300)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

#Strahlungsdaten laden: hier Verwendung der Strahlungsdaten vom Sensor unter Wasser der Sonnenstation 
# (passt besser, da Strahlung zeitlich vor Sauerstoffanstieg steigt)
df_rad = pd.read_csv("plot_series_with_cos_replacement_from_2025-08-04.csv",
                     parse_dates=["timestamp"], sep=',')
df_rad = df_rad.rename(columns={"timestamp": "time","S2_plot_blended": "Radiation"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültigen Strahlungswerten verwenden
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten auf Zeitstempel der Sauerstoffdaten legen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

# Definition der Daten für den Modellfit
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values  # Zeit in Sekunden
y_data = df_filtered['DO (mg/l)'].values                                                # Sauerstoffwerte

rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values                                            # Strahlungswerte

# Fit-Berechnungen
# Startwerte für die Parameter
p0_linear = [y_data[0], 1e-8, 1e-10, 1e-5]      # Lineares Modell
p0_mm     = [y_data[0], 1e-3, 100, 1e-10, 1e-9] # Michaelis-Menten Modell

# Modellfit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))  # Achsenbeschriftung Datum/Zeit

# Plotten der Fits
# Erzeugung gleichmäßig verteilter Zeitpunkte, auf denen das Modell ausgewertet wird
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
# Umwandlung der Zeitpunkte in echte Zeitstempel
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Linearer Fit: Modellgleichung zum Plotten
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Fit: Modellgleichung zum Plotten
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) /
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen kombinieren
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=18)

# Layout & Anzeige
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()

#%% Messung: Schattenbox vom 6.-7.8.2025
# Sauerstoffdaten einlesen
df1 = read("Messung3Schatten.txt")
df2 = read("Messung3.2Schatten.txt")

# Zusammenfügen & Zeitstempel anpassen
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]   # relative Zeit ab erster Messung
start_datetime = pd.Timestamp("2025-08-06 15:57:00")                # Startzeitpunkt der Messung
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Kürzen der Daten auf den relevanten Zeitraum
start_time = df['Time'].iloc[0] + timedelta(minutes=400)
end_time   = df['Time'].iloc[-1] - timedelta(minutes=90)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: Hier Verwendung der Strahlungsdaten vom Sensor unter Wasser der Dunkelstation
df_rad = pd.read_csv("dunkelstation_final.csv", parse_dates=["time"], sep=';')
df_rad = df_rad.rename(columns={"time": "time", "Dunkelstation_2_Neu": "Radiation"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültiger Strahlung behalten (keine NaN-Werte)
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungswerte den Sauerstoffzeitpunkten zuordnen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

# Definition der Daten für den Modellfit
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values  # Zeit in Sekunden
y_data = df_filtered['DO (mg/l)'].values                                                # Sauerstoffwerte
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values                                            # Strahlungswerte

#Fit-Berechnungen
# Startwerte für die Parameter
p0_linear = [y_data[0], 1e-6, 1e-9, 1e-8]               # Lineares Modell
p0_mm     = [y_data[0], 1e-9, 1e-6, 1e-9, 1e-7]         # Michaelis-Menten Modell (Beispielwerte)

# Modellfit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm     = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))  # Achsenbeschriftung Datum/Zeit

# Plotten der Fits
# Zeitpunkte für die Modellkurven
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Lineares Modell für den Plot
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Modell für den Plot
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) /
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05))
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen kombinieren
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=18)

# Layout & Anzeige
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()
#%% Messung: Sonnenbox vom 7.-8.8.2025
#Sauerstoffdaten einlesen
df1 = read("Messung4Sonne.txt")
df2 = read("Messung4.2Sonne.txt")

# Zusammenfügen & Zeitstempel anpassen
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]
start_datetime = pd.Timestamp("2025-08-07 16:28:00")
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Kürzen der Daten auf den relevanten Zeitraum
start_time = df['Time'].iloc[0] + timedelta(minutes=300)
end_time = df['Time'].iloc[-1] - timedelta(minutes=380)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: hier Verwendung der Strahlungsdaten vom Sensor unter Wasser der Sonnenstation (passt besser, Strahlung steigt zeitlich vor Sauerstoff)
df_rad = pd.read_csv("plot_series_with_cos_replacement_from_2025-08-04.csv",parse_dates=["timestamp"])
df_rad = df_rad.rename(columns={"timestamp": "time","S2_plot_blended": "Radiation"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültiger Radiation behalten (keine NaN Werte)
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten zeitlich zu Sauerstoffdaten anpassen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

# Definition der Daten für den Modellfit
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
y_data = df_filtered['DO (mg/l)'].values
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values

# Fit-Berechnungen
# Startwerte 
p0_linear = [y_data[0], 1e-8, 1e-9, 1e-6] # Lineares Modell
p0_mm = [y_data[0], 1e-3, 10, 1e-9, 1e-4]  # Michaelis-Menten Modell

# Modellfit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

# Plotten der Fits
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Lineares Modell für den Plot
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Modell für den Plot
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) / 
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=18)

# Layout & Anzeige
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()
#%% Messung: Schattenbox vom 7.-8.8.2025
# Sauerstoffdaten einlesen
df1 = read("Messung4Schatten.txt")
df2 = read("Messung4.2Schatten.txt")

# Dateien zusammenfügen & Zeitstempel anpassen
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]
start_datetime = pd.Timestamp("2025-08-07 16:46:00")
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Daten kürzen auf relevanten Zeitreihe
start_time = df['Time'].iloc[0] + timedelta(minutes=250)
end_time = df['Time'].iloc[-1] - timedelta(minutes=90)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: hier Verwendung der Strahlungsdaten vom Sensor unter Wasser der Dunkelstation
df_rad = pd.read_csv("dunkelstation_final.csv",parse_dates=["time"], sep=';')
df_rad = df_rad.rename(columns={"time": "time","Dunkelstation_2_Neu": "Radiation"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültiger Radiation behalten (keine NaN Werte)
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten zeitlich zu Sauerstoffdaten anpassen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

# Daten für den Modellfit definieren
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
y_data = df_filtered['DO (mg/l)'].values
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values

# Fit-Berechnungen
# Lineares Modell
p0_linear = [y_data[0], 1e-6, 1e-8, 1e-7]  #Startwerte

# Michaelis-Menten Modell
p0_mm = [y_data[0], 1e-3, 10, 1e-8, 1e-8] #Startwerte

# Fit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

# Plotten der Fits
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Linearer Fit für Plot aus Funktion herausziehen
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Fit für Plot aus Funktion herausziehen
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) / 
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=18)

# Anzeige und Layout
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()
#%% Messung: Sonnenbox vom 8.-9.8.2025
#Sauerstoffdaten einlesen
df1 = read("Messung5Sonne.txt")
df2 = read("Messung5.2Sonne.txt")

# Dateien zusammfügen und Zeitstempel korrigieren
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]
start_datetime = pd.Timestamp("2025-08-08 18:23:00")
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Daten auf relevante Zeiten kürzen
start_time = df['Time'].iloc[0] + timedelta(minutes=150)
end_time = df['Time'].iloc[-1] - timedelta(minutes=420)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: Verwendung der Daten des Sensors aus der Box 
df_rad = pd.read_csv("merged_Dunkel_S2__Pflanze_S1.txt",parse_dates=["timestamp_europe_berlin"])
df_rad = df_rad.rename(columns={"timestamp_europe_berlin": "time","pflanzenstation_sensor1_w_m2": "Radiation","dunkelstation_sensor2_w_m2": "Radiation1"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültiger Radiation behalten (keine NaN Werte)
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten zeitlich zu Sauerstoffdaten anpassen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

# Daten für Modellfit definieren
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
y_data = df_filtered['DO (mg/l)'].values
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values

# Fit-Berechnungen
# Lineares Modell
p0_linear = [y_data[0], 1e-10, 1e-4, 1e-7]  # Startwerte

# Michaelis-Menten Modell
p0_mm = [y_data[0], 1e-3, 100, 1e-2, 1e-4] #Startwerte

# Fit-Funktionen aufrufen 
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

# Plotten der Fits
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Linearer Fit für Plot aus der Funktion extrahieren
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Fit für Plot aus der Funktion extrahieren
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) / 
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=18)

# Anzeige & Layout
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()
#%% Messung: Schattenbox vom 8.-9.8.2025
#Sauerstoffdaten einlesen
df1 = read("Messung5Schatten.txt")
df2 = read("Messung5.2Schatten.txt")

# Zusammenfügen der Dateien und Zeitstempel korrigieren
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]
start_datetime = pd.Timestamp("2025-08-08 18:44:00")
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Kürzen der Daten auf relevante Messbereiche
start_time = df['Time'].iloc[0] + timedelta(minutes=380)
end_time = df['Time'].iloc[-1] - timedelta(minutes=4)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: hier Verwendung der Strahlungsdaten vom Sensor unter Wasser der Dunkelstation
df_rad = pd.read_csv("dunkelstation_final.csv",parse_dates=["time"], sep=';')
df_rad = df_rad.rename(columns={"time": "time","Dunkelstation_2_Neu": "Radiation"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültiger Radiation behalten (keine NaN Werte)
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten zeitlich zu Sauerstoffdaten anpassen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
y_data = df_filtered['DO (mg/l)'].values
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values

# Fit-Berechnungen
# Lineares Modell
p0_linear = [y_data[0], 1e-9, 1e-6, 1e-8]  #  Startwerte

# Michaelis-Menten Modell
p0_mm = [y_data[0], 1e-1, 100, 1e-8, 1e-9] #Startwerte

# Fit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

# Plotten der Fits
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Linearer Fit aus Funktion zum Plotten herausziehen
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"])
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Fit aus Funktion zum Plotten herausziehen
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) / 
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=18)

# Anzeige & Layout
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()
#%% Messung: Sonnenbox vom 9.-10.8.2025
#Sauerstoffdaten einlesen
df1 = read("Messung6Sonne.txt")
df2 = read("Messung6.2Sonne.txt")

#Zusammenfügen der Dateien und Anpassung des Zeitstempels
df = pd.concat([df1, df2]).sort_values(by='Time (sec)').reset_index(drop=True)
df['RelativeTime'] = df['Time (sec)'] - df['Time (sec)'].iloc[0]
start_datetime = pd.Timestamp("2025-08-09 19:33:00")
df['Time'] = start_datetime + pd.to_timedelta(df['RelativeTime'], unit='s')

# Kürzen der Daten auf den relevanten Messbereich
start_time = df['Time'].iloc[0] + timedelta(minutes=100)
end_time = df['Time'].iloc[-1] - timedelta(minutes=470)
df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)].copy()

# Strahlungsdaten laden: hier Verwendung der Strahlungsdaten vom Sensor unter Wasser der Sonnenstation (passt besser, Strahlung steigt zeitlich vor Sauerstoff)
df_rad = pd.read_csv("plot_series_with_cos_replacement_from_2025-08-04.csv",parse_dates=["timestamp"])
df_rad = df_rad.rename(columns={"timestamp": "time","S2_plot_blended": "Radiation"})

# Zeitzone entfernen
df_rad["time"] = df_rad["time"].dt.tz_localize(None)

# Nur Zeilen mit gültiger Radiation behalten (keine NaN Werte)
df_rad = df_rad.dropna(subset=["Radiation"])

# Interpolation: Strahlungsdaten zeitlich zu Sauerstoffdaten anpassen
df_rad_interp = df_rad.set_index("time").reindex(df_filtered["Time"], method="nearest", tolerance=pd.Timedelta("2min"))
df_filtered.loc[:, "Radiation"] = df_rad_interp["Radiation"].values

#Definition der Daten des Modellfits
t_data = (df_filtered['Time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
y_data = df_filtered['DO (mg/l)'].values
rad_times_full = (df_rad['time'] - df_filtered['Time'].iloc[0]).dt.total_seconds().values
rad_values_full = df_rad['Radiation'].values

# Fit-Berechnungen
# Lineares Modell
p0_linear = [y_data[0], 1e-8, 1e-6, 1e-7]  #Startwerte

# Michaelis-Menten Modell
p0_mm = [y_data[0], 1e-4, 100, 1e-5, 1e-9]  # Startwerte

# Fit-Funktionen aufrufen
result_linear = fit_do_linear_model(t_data, y_data, rad_times_full, rad_values_full, p0_linear)
result_mm = fit_do_mm_model(t_data, y_data, rad_times_full, rad_values_full, p0_mm)

# Parameterwerte ausgeben
print("\n--- Lineares Modell ---")
names_linear = ["DO0", "k_photo", "r_zehr_max", "K_M"]
for n, p, e in zip(names_linear, result_linear["params"], result_linear["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_linear["rmse"])

print("\n--- Michaelis-Menten Modell ---")
names_mm = ["DO0", "r_photo_max", "R_05", "r_zehr_max", "K_M"]
for n, p, e in zip(names_mm, result_mm["params"], result_mm["perr"]):
    print(f"{n:12s} = {p:12.5e} ± {e:.2e}")
print("RMSE:", result_mm["rmse"])

# Plot-Erstellung
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plotten der Messdaten
ax1.plot(df_filtered['Time'], y_data, '*:', color='b', label="Messdaten", markersize=6, mew=2)
ax1.set_xlabel("Zeit", fontsize=22)
ax1.set_ylabel(r"Gelöster Sauerstoff mg L$^{-1}$", color='b', fontsize=22)
ax1.tick_params(axis='y', labelcolor='b', labelsize=18)
ax1.tick_params(axis='x', labelsize=18)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

# Plotten der Fits
t_fit = np.linspace(t_data.min(), t_data.max(), 500)
time_fit = df_filtered['Time'].iloc[0] + pd.to_timedelta(t_fit, unit='s')

# Linearer Fit aus Funktion zum Plotten herausziehen
def do_model_linear_plot(t_eval, DO0, k_photo, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: (k_photo * np.interp(t, rad_times_full, rad_values_full) -
                           r_zehr_max * DO / (K_M + DO)),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval)
    return sol.y[0]

y_fit_linear = do_model_linear_plot(t_fit, *result_linear["params"] )
ax1.plot(time_fit, y_fit_linear, '-', color='c', label="Lineares Gesetz", linewidth=2.5)

# Michaelis-Menten Fit zum PLotten aus Funktion herausziehen
def do_model_mm_plot(t_eval, DO0, r_photo_max, R_05, r_zehr_max, K_M):
    sol = solve_ivp(
        fun=lambda t, DO: r_photo_max * (np.interp(t, rad_times_full, rad_values_full) / 
                                         (np.interp(t, rad_times_full, rad_values_full) + R_05)) 
                          - r_zehr_max * DO / (K_M + DO),
        t_span=(t_eval[0], t_eval[-1]),
        y0=[DO0],
        t_eval=t_eval
    )
    return sol.y[0]

y_fit_mm = do_model_mm_plot(t_fit, *result_mm["params"])
ax1.plot(time_fit, y_fit_mm, '--', color='#8B0000', label="Michaelis-Menten-Gesetz", linewidth=2.5, markersize=8)

# Zweite Y-Achse für Strahlung
ax2 = ax1.twinx()
ax2.plot(df_filtered['Time'], df_filtered['Radiation'], '-', color='purple', label='Strahlung', alpha=0.7, linewidth=2)
ax2.set_ylabel(r"Strahlung W m$^{-1}$", color='purple', fontsize=22)
ax2.tick_params(axis='y', labelcolor='purple', labelsize=18)

# Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=18)

# Layout & Anzeige
plt.grid(True)
plt.gcf().autofmt_xdate(rotation=30, ha="right")
plt.tight_layout()
plt.show()