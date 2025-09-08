# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 14:25:27 2025

@author: lenny

Beschreibung:
    - Berechnet Abschwächungsfaktoren (Lambert-Beer) aus Wassertiefen
    - Wendet die Faktoren auf eine Strahlungsmatrix an
    - Speichert die abgeschwächte Matrix als CSV
"""

import pandas as pd
import numpy as np

# --- Parameter ---
input_tiefen_csv = "ammer_10m_wassertiefen.csv"   # Eingabe-Datei Wassertiefen
input_matrix_csv = "matrix_strahlung_ueber_wasser.csv"   # Original-Matrix (time + Segmente)
output_matrix_csv = "matrix_strahlung_unter_wasser.csv" # Ergebnis
k = 4   # Extinktionskoeffizient in 1/m

# ======================================================
# 1) Abschwächungsfaktoren berechnen
# ======================================================
df_tiefen = pd.read_csv(input_tiefen_csv)

# Wassertiefe in Meter
df_tiefen["Wassertiefe_m"] = df_tiefen["Wassertiefe"] / 100.0

# Lambert-Beer Abschwächung
df_tiefen["Abschwaechung"] = np.exp(-k * df_tiefen["Wassertiefe_m"])

# Dictionary für spätere Anwendung
absch_dict = dict(zip(df_tiefen["fluss_idx"], df_tiefen["Abschwaechung"]))

# ======================================================
# 2) Strahlungsmatrix einlesen und Abschwächung anwenden
# ======================================================
df_matrix = pd.read_csv(input_matrix_csv)

for col in df_matrix.columns:
    if col != "time":
        idx = int(col)  # Spaltenname als Zahl interpretieren
        if idx in absch_dict:
            # multiplizieren, dann floor und int
            df_matrix[col] = np.floor(df_matrix[col] * absch_dict[idx]).astype(int)

# ======================================================
# 3) Ausgabe speichern
# ======================================================
df_matrix.to_csv(output_matrix_csv, index=False)

print(f"✅ Matrix erfolgreich abgeschwächt, gefloort und gespeichert in '{output_matrix_csv}'")
