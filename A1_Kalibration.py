# Umweltnaturwissenschaftliches Feldpraktikum 

# Gruppe A1: Stefanie Frey und Christina Trueck

# Kalibration der Sauerstoffdaten der Logger mithilfe der Winklermessungen:
# Kalibration 1 im Labor vor Beginn der Messphase und Kalibration 2 im Feld am Ende der Messphase

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

## Daten einlesen
# Winkler-Ergebnisse einlesen
df = pd.read_csv("O2_Winkler [mgL].txt")

# Logger Datensaetze einlesen
df1_viel = pd.read_csv('Logger1_2025-07-31 144500Z.txt',header=0)
df1_wenig_und_mittel = pd.read_csv('Logger1_2025-08-01 144500Z.txt',header=0)
df2_viel = pd.read_csv('Logger2_2025-07-31 144500Z.txt',header=0)
df2_wenig_und_mittel = pd.read_csv('Logger2_2025-08-01 144500Z.txt',header=0)
df3_viel = pd.read_csv('Logger3_2025-07-31 144600Z.txt',header=0)
df3_wenig_und_mittel = pd.read_csv('Logger3_2025-08-01 144600Z.txt',header=0)
df4_viel = pd.read_csv('Logger4_2025-07-31 144600Z.txt',header=0)
df4_wenig_und_mittel = pd.read_csv('Logger4_2025-08-01 144600Z.txt',header=0)
df5_viel = pd.read_csv('Logger5_2025-07-31 144500Z.txt',header=0)
df5_wenig_und_mittel = pd.read_csv('Logger5_2025-08-01 144500Z.txt',header=0)

df1 = pd.read_csv('Felddaten Logger 1.txt',header=0)
df2 = pd.read_csv('Felddaten Logger 2.txt',header=0)
df3 = pd.read_csv('Felddaten Logger 3.txt',header=0)
df4 = pd.read_csv('Felddaten Logger 4.txt',header=0)
df5 = pd.read_csv('Felddaten Logger 5.txt',header=0)
df6 = pd.read_csv("Felddaten Logger GB 83.txt",header=0)
df7 = pd.read_csv("Felddaten Logger GB 39.txt",header=0)


#%%
## Sauerstoffkonzentrationen der Logger mitteln und zum DataFrame mit den Winkler-Daten hinzfuegen
## Kalibration 1 - viel Sauerstoff

# Bereich definieren, in dem die Winklerproben genommen wurden und ueber den die Sauerstoffkonzentration gemittelt wird
start = 1754053560
ende = 1754054580

# Logger 1
bereich = df1_viel[(df1_viel['Time (sec)']>= start)&(df1_viel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[0,'Logger 1'] = mittelwert # Mittelwert in 1. Zeile der Spalte 'Logger 1' speichern

# Logger 2
bereich = df2_viel[(df2_viel['Time (sec)']>= start)&(df2_viel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[0,'Logger 2'] = mittelwert # Mittelwert in 1. Zeile der Spalte 'Logger 2' speichern

# Logger 3
bereich = df3_viel[(df3_viel['Time (sec)']>= start)&(df3_viel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[0,'Logger 3'] = mittelwert # Mittelwert in 1. Zeile der Spalte 'Logger 3' speichern

# Logger 4
bereich = df4_viel[(df4_viel['Time (sec)']>= start)&(df4_viel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[0,'Logger 4'] = mittelwert # Mittelwert in 1. Zeile der Spalte 'Logger 4' speichern

# Logger 5
bereich = df5_viel[(df5_viel['Time (sec)']>= start)&(df5_viel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[0,'Logger 5'] = mittelwert # Mittelwert in 1. Zeile der Spalte 'Logger 5' speichern

#%%
## Kalibration 1 - wenig Sauerstoff

# Bereich definieren, in dem die Winklerproben genommen wurden und ueber den die Sauerstoffkonzentration gemittelt wird
start = 1754071980
ende = 1754072940

# Logger 1
bereich = df1_wenig_und_mittel[(df1_wenig_und_mittel['Time (sec)']>= start)&(df1_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[1,'Logger 1'] = mittelwert # Mittelwert in 2. Zeile der Spalte 'Logger 1' speichern

# Logger 2
bereich = df2_wenig_und_mittel[(df2_wenig_und_mittel['Time (sec)']>= start)&(df2_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[1,'Logger 2'] = mittelwert # Mittelwert in 2. Zeile der Spalte 'Logger 2' speichern

# Logger 3
bereich = df3_wenig_und_mittel[(df3_wenig_und_mittel['Time (sec)']>= start)&(df3_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[1,'Logger 3'] = mittelwert # Mittelwert in 2. Zeile der Spalte 'Logger 3' speichern

# Logger 4
bereich = df4_wenig_und_mittel[(df4_wenig_und_mittel['Time (sec)']>= start)&(df4_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[1,'Logger 4'] = mittelwert # Mittelwert in 2. Zeile der Spalte 'Logger 4' speichern

# Logger 5
bereich = df5_wenig_und_mittel[(df5_wenig_und_mittel['Time (sec)']>= start)&(df5_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[1,'Logger 5'] = mittelwert # Mittelwert in 2. Zeile der Spalte 'Logger 5' speichern

#%%
## Kalibration 1 - mittel Sauerstoff

# Bereich definieren, in dem die Winklerproben genommen wurden und ueber den die Sauerstoffkonzentration gemittelt wird
start = 1754080440
ende = 1754081160

# Logger 1
bereich = df1_wenig_und_mittel[(df1_wenig_und_mittel['Time (sec)']>= start)&(df1_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[2,'Logger 1'] = mittelwert # Mittelwert in 3. Zeile der Spalte 'Logger 1' speichern

# Logger 2
bereich = df2_wenig_und_mittel[(df2_wenig_und_mittel['Time (sec)']>= start)&(df2_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[2,'Logger 2'] = mittelwert # Mittelwert in 3. Zeile der Spalte 'Logger 2' speichern

# Logger 3
bereich = df3_wenig_und_mittel[(df3_wenig_und_mittel['Time (sec)']>= start)&(df3_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[2,'Logger 3'] = mittelwert # Mittelwert in 3. Zeile der Spalte 'Logger 3' speichern

# Logger 4
bereich = df4_wenig_und_mittel[(df4_wenig_und_mittel['Time (sec)']>= start)&(df4_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[2,'Logger 4'] = mittelwert # Mittelwert in 3. Zeile der Spalte 'Logger 4' speichern

# Logger 5
bereich = df5_wenig_und_mittel[(df5_wenig_und_mittel['Time (sec)']>= start)&(df5_wenig_und_mittel['Time (sec)']<= ende)]
mittelwert = bereich['  DO (mg/l)'].mean()
df.loc[2,'Logger 5'] = mittelwert # Mittelwert in 3. Zeile der Spalte 'Logger 5' speichern


#%%
## Kalibration 2 - viel Sauerstoff

# Bereich definieren, in dem die Winklerproben genommen wurden und ueber den die Sauerstoffkonzentration gemittelt wird
start = 1755177120
ende = 1755178920

# Logger 1
bereich = df1[(df1['Time (sec)']>= start)&(df1['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 1'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 1' speichern

# Logger 2
bereich = df2[(df2['Time (sec)']>= start)&(df2['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 2'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 2' speichern

# Logger 3
bereich = df3[(df3['Time (sec)']>= start)&(df3['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 3'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 3' speichern

# Logger 4
bereich = df4[(df4['Time (sec)']>= start)&(df4['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 4'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 4' speichern

# Logger 5
bereich = df5[(df5['Time (sec)']>= start)&(df5['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 5'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 5' speichern

# Logger 6 (GB 83 neben Logger 5)
df6['Time (sec)'] = df6['Time (sec)'] + 7185452 # Timeshift des Unixcodes korrigieren

bereich = df6[(df6['Time (sec)']>= start)&(df6['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 6'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 6' speichern

# Logger 7 (GB 39 in der Stroemung)
df7['Time (sec)'] = df7['Time (sec)'] + 10808102 # Timeshift des Unixcodes korrigieren

bereich = df7[(df7['Time (sec)']>= start)&(df7['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[3,'Logger 7'] = mittelwert # Mittelwert in 4. Zeile der Spalte 'Logger 7' speichern

#%%
## Kalibration 2 - wenig Sauerstoff

# Bereich definieren, in dem die Winklerproben genommen wurden und ueber den die Sauerstoffkonzentration gemittelt wird
start = 1755231720
ende = 1755233760

# Logger 1
bereich = df1[(df1['Time (sec)']>= start)&(df1['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 1'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 1' speichern

# Logger 2
bereich = df2[(df2['Time (sec)']>= start)&(df2['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 2'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 2' speichern

# Logger 3
bereich = df3[(df3['Time (sec)']>= start)&(df3['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 3'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 3' speichern

# Logger 4
bereich = df4[(df4['Time (sec)']>= start)&(df4['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 4'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 4' speichern

# Logger 5
bereich = df5[(df5['Time (sec)']>= start)&(df5['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 5'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 5' speichern

# Logger 6 (GB 83 neben Logger 5)
bereich = df6[(df6['Time (sec)']>= start)&(df6['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 6'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 6' speichern

# Logger 7 (GB 39 in der Stroemung)
bereich = df7[(df7['Time (sec)']>= start)&(df7['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[4,'Logger 7'] = mittelwert # Mittelwert in 5. Zeile der Spalte 'Logger 7' speichern

#%%
## Kalibration 2 - mittel Sauerstoff

# Bereich definieren, in dem die Winklerproben genommen wurden und ueber den die Sauerstoffkonzentration gemittelt wird
start = 1755248280
ende = 1755249840

# Logger 1
bereich = df1[(df1['Time (sec)']>= start)&(df1['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 1'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 1' speichern

# Logger 2
bereich = df2[(df2['Time (sec)']>= start)&(df2['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 2'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 2' speichern

# Logger 3
bereich = df3[(df3['Time (sec)']>= start)&(df3['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 3'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 3' speichern

# Logger 4
bereich = df4[(df4['Time (sec)']>= start)&(df4['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 4'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 4' speichern

# Logger 5
bereich = df5[(df5['Time (sec)']>= start)&(df5['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 5'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 5' speichern

# Logger 6 (GB 83 neben Logger 5)
bereich = df6[(df6['Time (sec)']>= start)&(df6['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 6'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 6' speichern

# Logger 7 (GB 39 in der Stroemung)
bereich = df7[(df7['Time (sec)']>= start)&(df7['Time (sec)']<= ende)]
mittelwert = bereich['DO (mg/l)'].mean()
df.loc[5,'Logger 7'] = mittelwert # Mittelwert in 6. Zeile der Spalte 'Logger 7' speichern


#%%
## Logger- und Winkler-Daten beider Kalibrationen plotten

# Daten zuordnen
x = "O2_Winkler [mg/L]"
logger_cols = ["Logger 1", "Logger 2", "Logger 3", "Logger 4", "Logger 5", "Logger 6", "Logger 7"]

# Farbzuordnung
farben = {
    "Logger 1": "darkorange",
    "Logger 2": "yellowgreen",
    "Logger 3": "deepskyblue",
    "Logger 4": "purple",
    "Logger 5": "darkgreen",
    "Logger 6": "gold",
    "Logger 7": "crimson"
}

# Plot erstellen
plt.figure(figsize=(16,8))

for col in logger_cols:
  
    # Kalibration 1 (Zeilen 0-2, Kreise): 
    plt.scatter(df.loc[0:2, x], df.loc[0:2, col], marker="o", facecolors="none", color=farben[col], s=70)

    # Kalibration 2 (Zeilen 3-5, Kreuze): 
    plt.scatter(df.loc[3:5, x], df.loc[3:5, col], marker="x", color=farben[col], s=70)  
    
# Marker erstellen fuer Erklaerung in Legende
plt.scatter([], [], color="black", marker="o", facecolors="none", label="Kalibration 1")
plt.scatter([], [], color="black", marker="x", label="Kalibration 2")


# Lineare Regression (fuer jeden Logger Kalibration 1 und 2 kombiniert)
gleichungen = {}

for col in logger_cols:
    
    # NaN-Werte entfernen
    sub = df[[x, col]].dropna()

    # Lineare Regression
    steigung, achsenabschnitt, r_wert, p_wert, std_err = linregress(sub[x], sub[col])

    # Trendlinien erstellen
    x_vals = np.linspace(sub[x].min(), sub[x].max(), 100)
    y_vals = steigung * x_vals + achsenabschnitt
    plt.plot(x_vals, y_vals, color=farben[col], linestyle="--", linewidth=1, label=f'{col}: y = {steigung:.3f}x + {achsenabschnitt:.3f}, R² = {r_wert**2:.4f}')

    # Gleichungen speichern
    gleichungen[col] = f"y = {steigung:.3f}x + ({achsenabschnitt:.3f})"

    # Gleichungen ausgeben
    print(f"{col}: y = {steigung:.3f}x + {achsenabschnitt:.3f}, R² = {r_wert**2:.4f}")

plt.xlabel(r'Winkler $c({\mathrm{O_2}})~\mathrm{[mg~L^{-1}]}$',fontsize=18)
plt.ylabel(r"Logger $c({\mathrm{O_2}})~\mathrm{[mg~L^{-1}]}$",fontsize=18)
plt.tick_params(axis='both',labelsize=15) 
plt.legend(loc='upper left',fontsize=16)
plt.grid(True)
plt.show()

#%%

## Kalibration der Felddaten und Erstellen der kalibrierten Datensaetzen 

# Ergebnisse der linearen Regression speichern
regressionsergebnisse = {}

for col in logger_cols:
    slope, intercept, r_value, p_value, std_err = linregress(df[x], df[col])
    regressionsergebnisse[col] = {"slope": slope,"intercept": intercept,"R2": r_value**2}


# Logger 1

# Werte der linearen Regression definieren
steigung1 = regressionsergebnisse["Logger 1"]["slope"]
achsenabschnitt1 = regressionsergebnisse["Logger 1"]["intercept"]

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df1["DO (mg/l)"] = ((df1["DO (mg/l)"] + achsenabschnitt1) / steigung1)

# Neue Datei mit kalibriertem Datensatz speichern
df1.to_csv("Felddaten Logger 1_kalibriert.txt", index=False, float_format="%.3f")


# Logger 2

# Werte der linearen Regression definieren
steigung2 = regressionsergebnisse["Logger 2"]["slope"]
achsenabschnitt2 = regressionsergebnisse["Logger 2"]["intercept"]

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df2["DO (mg/l)"] = ((df2["DO (mg/l)"] + achsenabschnitt2) / steigung2)

# Neue Datei mit kalibriertem Datensatz speichern
df2.to_csv("Felddaten Logger 2_kalibriert.txt", index=False, float_format="%.3f")


# Logger 3

# Werte der linearen Regression definieren
steigung3 = regressionsergebnisse["Logger 3"]["slope"]
achsenabschnitt3 = regressionsergebnisse["Logger 3"]["intercept"]

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df3["DO (mg/l)"] = ((df3["DO (mg/l)"] + achsenabschnitt3) / steigung3)

# Neue Datei mit kalibriertem Datensatz speichern
df3.to_csv("Felddaten Logger 3_kalibriert.txt", index=False, float_format="%.3f")


# Logger 4

# Werte der linearen Regression definieren
steigung4 = regressionsergebnisse["Logger 4"]["slope"]
achsenabschnitt4 = regressionsergebnisse["Logger 4"]["intercept"]

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df4["DO (mg/l)"] = ((df4["DO (mg/l)"] + achsenabschnitt4) / steigung4)

# Neue Datei mit kalibriertem Datensatz speichern
df4.to_csv("Felddaten Logger 4_kalibriert.txt", index=False, float_format="%.3f")


# Logger 5

# Werte der linearen Regression definieren
steigung5 = regressionsergebnisse["Logger 5"]["slope"]
achsenabschnitt5 = regressionsergebnisse["Logger 5"]["intercept"]

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df5["DO (mg/l)"] = ((df5["DO (mg/l)"] + achsenabschnitt5) / steigung5)

# Neue Datei mit kalibriertem Datensatz speichern
df5.to_csv("Felddaten Logger 5_kalibriert.txt", index=False, float_format="%.3f")


# Logger 6 (GB 83 neben Logger 5)

# Werte der linearen Regression definieren
steigung6 = 1.1356
achsenabschnitt6 = 0.9286

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df6["DO (mg/l)"] = ((df6["DO (mg/l)"] + achsenabschnitt6) / steigung6)

# Neue Datei mit kalibriertem Datensatz speichern
df6.to_csv("Felddaten Logger GB 83_kalibriert.txt", index=False, float_format="%.3f")


# Logger (GB 39 in der Stroemung)

# Werte der linearen Regression definieren
steigung7 = 1.1632
achsenabschnitt7 = 0.7303

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df7["DO (mg/l)"] = ((df7["DO (mg/l)"] + achsenabschnitt7) / steigung7)

# Neue Datei mit kalibriertem Datensatz speichern
df7.to_csv("Felddaten Logger GB 39_kalibriert.txt", index=False, float_format="%.3f")





