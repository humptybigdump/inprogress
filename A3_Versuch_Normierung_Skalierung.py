# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 12:18:47 2025

@author: Elisa Nawrot
"""
import pandas as pd
import numpy as np

# Maße der Messbox
laenge_box_cm = 28 # cm
tiefe_box_cm = 19 # cm
hoehe_box_cm = 19.5 # cm
volumen_box_cm3 = laenge_box_cm * tiefe_box_cm * hoehe_box_cm # cm^3

# Umrechnung in Meter
h_box_m = hoehe_box_cm / 100 # m
volumen_box_m3 = volumen_box_cm3 / (100**3) # m^3

# Pflanzenanteile
f_box_sonne = 0.1500 # Pflanzenanteil in der Sonnen-Box (15%)
f_box_schatten = 0.1165 # Pflanzenanteil der Schatten-Box (11.65%)
f_ammer = 0.07 # Pflanzenanteil in der Ammer (7%)

# Blattoberfläche in den Boxen
a_leaf_sonne_cm2 = 434.7742 # cm^2
a_leaf_schatten_cm2 = 337.578087 # cm^2
a_leaf_sonne_m2 = a_leaf_sonne_cm2 / (100**2) # m^2
a_leaf_schatten_m2 = a_leaf_schatten_cm2 / (100**2) # m^2

# Maße der Ammer
h_ammer_cm = 43.52 # mittlere Ammertiefe in cm
b_ammer_cm = 450 # angeschätzte Ammerbreite in cm
l_ammer_cm = 3039.02 * 100 # betrachtete Ammerlänge in cm

# Umrechnung in Meter
h_ammer_m = h_ammer_cm / 100 # m
b_ammer_m = b_ammer_cm / 100 # m
l_ammer_m = l_ammer_cm / 100 # m

# Volumen der Ammer
volumen_ammer_m3 = h_ammer_m * b_ammer_m * l_ammer_m # m^3

# Blattoberfläche der Ammer, proportional zum Volumen und Pflanzenanteil
# Vereinfachte Annahme
a_leaf_ammer_m2 = volumen_ammer_m3 * f_ammer / h_ammer_m

# Einlesen der Daten aus der Excel-Tabelle
# Verwenden von skiprows=2, um die Überschriften zu überspringen und direkt die Daten zu nehmen,
# Verwenden von nrows=8, um nur die Daten bis einschließlich Zeile 10 zu lesen
df_raw = pd.read_excel("A3_Parameter.xlsx", skiprows=2, header=None, nrows=9)

# Manuelles Zuweisen der Spaltennamen basierend auf der Spaltenreihenfolge
df = df_raw[[0, 1, 3, 8, 12]].copy()
df.columns = ['Messung', 'k_photo_linear', 'r_resp_linear', 'r_max_mm', 'r_resp_mm']

# Korrigieren der Datentypen, um sicherzustellen, dass die Spalten numerisch sind
df['k_photo_linear'] = pd.to_numeric(df['k_photo_linear'].astype(str).str.replace(',', '.'), errors='coerce')
df['r_resp_linear'] = pd.to_numeric(df['r_resp_linear'].astype(str).str.replace(',', '.'), errors='coerce')
df['r_max_mm'] = pd.to_numeric(df['r_max_mm'].astype(str).str.replace(',', '.'), errors='coerce')
df['r_resp_mm'] = pd.to_numeric(df['r_resp_mm'].astype(str).str.replace(',', '.'), errors='coerce')

# Normierung und Skalierung der Parameter für Sonne und Schatten
df_scaled = df.copy() # Erstelle eine Kopie, um die neuen Spalten hinzuzufügen

# Wiederholen über jede Zeile des DataFrames
for index, row in df_scaled.iterrows():
    #Prüfen, ob jeder Messungstyp ein String ist
    messung_typ = str(row['Messung'])
    
    # richtigen Pflanzenanteil und Blattoberfläche für die Box bestimmen
    if 'Sonne' in messung_typ:
        f_box = f_box_sonne
        a_leaf_box_m2 = a_leaf_sonne_m2
    else: # von Schatten ausgehen
        f_box = f_box_schatten
        a_leaf_box_m2 = a_leaf_schatten_m2

    # 1. Normierung der Parameter: p_norm = p * (h_box_m / h_ammer_m) * (f_ammer / f_box)
    df_scaled.loc[index, 'k_photo_linear_norm'] = row['k_photo_linear'] * (h_box_m / h_ammer_m) * (f_ammer / f_box)
    df_scaled.loc[index, 'r_resp_linear_norm'] = row['r_resp_linear'] * (h_box_m / h_ammer_m) * (f_ammer / f_box)
    df_scaled.loc[index, 'r_max_mm_norm'] = row['r_max_mm'] * (h_box_m / h_ammer_m) * (f_ammer / f_box)
    df_scaled.loc[index, 'r_resp_mm_norm'] = row['r_resp_mm'] * (h_box_m / h_ammer_m) * (f_ammer / f_box)

    # 2. Skalierung der Parameter
    # Verhältnis von Blattoberfläche zu Volumen für Box und Ammer berechnen
    ratio_leaf_vol_box = a_leaf_box_m2 / volumen_box_m3
    ratio_leaf_vol_ammer = a_leaf_ammer_m2 / volumen_ammer_m3

    # Skalierungsfaktor: 
    scaling_factor = ratio_leaf_vol_ammer / ratio_leaf_vol_box

    # Normierte Parameter skalieren
    df_scaled.loc[index, 'k_photo_linear_scaled'] = df_scaled.loc[index, 'k_photo_linear_norm'] * scaling_factor
    df_scaled.loc[index, 'r_resp_linear_scaled'] = df_scaled.loc[index, 'r_resp_linear_norm'] * scaling_factor
    df_scaled.loc[index, 'r_max_mm_scaled'] = df_scaled.loc[index, 'r_max_mm_norm'] * scaling_factor
    df_scaled.loc[index, 'r_resp_mm_scaled'] = df_scaled.loc[index, 'r_resp_mm_norm'] * scaling_factor

# Ausgabe der Ergebnisse
print("--- Berechnete Ergebnisse ---")
print("\nSkalierungsfaktor:")
print(f"Blattfläche-zu-Volumen-Verhältnis Box: {ratio_leaf_vol_box:.5e} m²/m³")
print(f"Blattfläche-zu-Volumen-Verhältnis Ammer: {ratio_leaf_vol_ammer:.5e} m²/m³")
print(f"Skalierungsfaktor: {scaling_factor:.5f}")

print("\nNormierte Parameter für die Ammer (mit h_box/h_ammer & f_ammer/f_box):")
print(df_scaled[['Messung', 'k_photo_linear_norm', 'r_resp_linear_norm', 'r_max_mm_norm', 'r_resp_mm_norm']].to_string(float_format="%.5e"))

print("\nSkalierte Parameter für die Ammer (mit zusätzlichem Blattfläche/Volumen-Faktor):")
print(df_scaled[['Messung', 'k_photo_linear_scaled', 'r_resp_linear_scaled', 'r_max_mm_scaled', 'r_resp_mm_scaled']].to_string(float_format="%.5e"))