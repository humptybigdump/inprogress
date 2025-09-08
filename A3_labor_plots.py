# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 21:04:24 2025

@author: Lara Wadlinger
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Laden der Excel-Datei mit den Labordaten
df = pd.read_excel(r"C:\Users\laraw\OneDrive\Documents\Studium\4. Semester\Feldpraktikum\Labordaten\FotosyntheseMessung2.xlsx", engine="openpyxl", skiprows=3)

#%% Photosynthese: Probe 1
#Auswählen der relevanten Daten 
df_1= df.iloc[0:8, [1, 2]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)", "Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce') #Sauerstoffkonzentarion
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce') #Zeit

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100) # 100 gleichmäßig verteilte x-Werte
y_fit = slope * x_fit + intercept #Regressionsgerade

#Plot erstellen
plt.figure(figsize=(12,7)) 
plt.scatter(x, y, marker='o', s=100, label='Messwerte')  
plt.plot(x_fit, y_fit, color='red',linewidth=4,label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)", fontsize=26)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.legend(fontsize=20)
plt.grid(True, linewidth=1.5)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe 1')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe 2
#Auswählen der relevanten Daten 
df_1 = df.iloc[0:8, [3, 4]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x1 = pd.to_numeric(df_1.iloc[:, 1], errors='coerce') 
y1 = pd.to_numeric(df_1.iloc[:, 0], errors='coerce') 

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x1, y1)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit1 = np.linspace(x1.min(), x1.max(), 100)
y_fit1 = slope * x_fit1 + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))  
plt.scatter(x, y, marker='o', s=100, label='Messwerte')  
plt.plot(x_fit, y_fit, color='red',linewidth=4,label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)", fontsize=26)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.legend(fontsize=20)
plt.grid(True, linewidth=1.5)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe 2')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe 3
#Auswählen der relevanten Daten
df_1 = df.iloc[0:8, [5, 6]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x2 = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y2 = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x2, y2)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit2 = np.linspace(x2.min(), x2.max(), 100)
y_fit2 = slope * x_fit2 + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte') 
plt.plot(x_fit, y_fit, color='red', linewidth=4, label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)", fontsize=26)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.legend(fontsize=20)
plt.grid(True, linewidth=1.5)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe 3')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe Ammerwasser (Blank)
#Auswählen der relevanten Daten
df_1 = df.iloc[0:8, [7, 8]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x3 = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y3 = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x3, y3)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit3 = np.linspace(x3.min(), x3.max(), 100)
y_fit3 = slope * x_fit3 + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x3, y3, marker='o', s=100, label='Messwerte')
plt.plot(x_fit3, y_fit3, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe Ammerwasser')
print(f"Steigung (m): {slope:.4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe 1 (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[23:34, [1, 2]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe 1 (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe 2 (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[23:34, [3, 4]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe 2 (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe 3 (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[23:34, [5, 6]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe 3 (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Photosynthese: Probe Ammerwasser (Blank) (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[23:34, [7, 8]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Photosynthese: Probe Ammerwasser (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Zehrung: Probe 1 (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[39:48, [1, 2]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Zehrung: Probe 1 (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Zehrung: Probe 2 (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[39:48, [3, 4]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Zehrung: Probe 2 (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Zehrung: Probe 3 (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[39:48, [5, 6]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Zehrung: Probe 3 (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")
#%% Zehrung: Probe Ammerwasser (Blank) (Versuch 2)
#Auswählen der relevanten Daten
df_1= df.iloc[39:48, [7, 8]]
# Spaltenüberschriften benennen
df_1.columns = ["O2 (mg/L)","Zeit (min)"]

# Umwandeln der Daten in numerische Werte
x = pd.to_numeric(df_1.iloc[:, 1], errors='coerce')
y = pd.to_numeric(df_1.iloc[:, 0], errors='coerce')

# Lineare Regression berechnen (Formel: y = m*x + b)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Berechnen der Ausgleichsgeraden für den Plot
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = slope * x_fit + intercept

#Plot erstellen
plt.figure(figsize=(12, 7))
plt.scatter(x, y, marker='o', s=100, label='Messwerte')
plt.plot(x_fit, y_fit, color='red', linewidth=4,
         label=f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_value**2:.4f}')
plt.xlabel("Zeit (min)",fontsize=26)
plt.tick_params(axis='both', labelsize=22)
plt.ylabel("Gelöster Sauerstoff (mg L$^{-1}$)", fontsize=26)
plt.legend(fontsize=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Variablen-Werte der Regression ausgeben
print('Zehrung: Probe Ammerwasser (Versuch 2)')
print(f"Steigung (m): {slope:.4f} ± {std_err:4f}")
print(f"y-Achsenabschnitt (b): {intercept:.4f}")
print(f"Bestimmtheitsmaß (R²): {r_value**2:.4f}")

