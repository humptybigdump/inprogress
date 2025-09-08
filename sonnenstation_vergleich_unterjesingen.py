import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Globale Schriftgröße für X-Ticklabels
plt.rcParams.update({'xtick.labelsize': 10})

# Dateien laden
df1 = pd.read_csv("sonnenstation_korrigiert_1min.csv", sep=None, engine="python")
df2 = pd.read_csv("Referenz Unterjesingen.csv", sep=None, engine="python")

# Spaltennamen säubern 
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Sonnenstation vorbereiten
df1["timestamp"] = pd.to_datetime(df1["timestamp"], errors="coerce").dt.tz_localize(None)
df1 = df1.dropna(subset=["timestamp"])
df1["S1_plot_blended"] = pd.to_numeric(df1["S1_plot_blended"], errors="coerce")

# Sonnenstation: auf 15 Minuten mitteln
s1_15 = df1.set_index("timestamp").resample("15min").mean(numeric_only=True).rename_axis("datetime")

# Referenz vorbereiten 
df2["datetime"] = pd.to_datetime(
    df2["Tag"] + " " + df2["Stunde"], format="%d.%m.%Y %H:%M", errors="coerce"
)

# SUM_GS200 robust in Zahlen umwandeln
if df2["SUM_GS200"].dtype == object:
    df2["SUM_GS200"] = pd.to_numeric(df2["SUM_GS200"].str.replace(",", "."), errors="coerce")
else:
    df2["SUM_GS200"] = pd.to_numeric(df2["SUM_GS200"], errors="coerce")

df2 = df2.dropna(subset=["datetime", "SUM_GS200"])

# Referenz: auf 15 Minuten hochsamplen und interpolieren
ref_15 = df2.set_index("datetime").resample("15min").interpolate(method="time")

# Startdatum festlegen (ab 04.08.2025) 
start_date = pd.to_datetime("2025-08-04")
s1_15 = s1_15[s1_15.index >= start_date]
ref_15 = ref_15[ref_15.index >= start_date]

# Gemeinsamer Zeitraum bestimmen
start = max(s1_15.index.min(), ref_15.index.min())
end = min(s1_15.index.max(), ref_15.index.max())

s1_15 = s1_15.loc[start:end]
ref_15 = ref_15.loc[start:end]

# Plot
plt.figure(figsize=(14,6))
plt.plot(s1_15.index, s1_15["S1_plot_blended"],
         label="Sonnenstation S1 (15-min Mittel)", alpha=0.9)
plt.plot(ref_15.index, ref_15["SUM_GS200"],
         label="Referenz Unterjesingen (interpoliert 15-min)", alpha=0.9)

plt.xlabel("Zeit (MESZ)")
plt.ylabel("Strahlung [W/m²]")
#plt.title("Sonnenstation S1 vs. Referenz – ab 04.08.2025 (Kurven)")
plt.legend()
plt.grid(True)

# X-Achse: Tick jeden Tag um 12 Uhr
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.HourLocator(byhour=12))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m %H:%M"))

# Ticklabel-Schrift normal, Rotation, Textende auf Tick
for label in ax.get_xticklabels():
    label.set_fontweight('normal')
    label.set_rotation(45)
    label.set_ha('right')  # Textende auf der Ticklinie ausrichten

plt.tight_layout()
plt.show()
