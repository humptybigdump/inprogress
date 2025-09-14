"""
Uebung 3.0 - Variablen

Hier stehen die Variablen, die allen Modulen zur Verfügung stehen sollen.

Autor: Mark-Patrick Mühlhausen

Datum: 2024-07-29
"""

# Defintion von globalen Variablen

# Geometrie
L1        = ?                 # [m]
L2        = ?                 # [m]
h         = ??               # [m] Stopfenlaenge
R         = ??               # [m] Rohrradius
s         = ??              # [m] Spalthoehe zwischen Rohr und Stopfen

# Wasser
muW       = ?             # [Pa s] bei 273K
rhoW      = ?              # [kg /m3]

# Luft
muL       = ?         # [Pa s] bei 273K
rhoL      = ?                 # [kg / m3]

# Stopfen aus Stahl
rhoS      = ?              # [kg / m3]

# Randbedingung
p0        = 100000            # [Pa] Umgebungsdruck
p1        = 800000            # [Pa] Druck der ploetzlich aufgepraegt wird

# Numerik
dt        = 1e-4              # [s] Zeitschrittweite
N         = int(1/dt)              # [-] Anzahl Zeitschritte