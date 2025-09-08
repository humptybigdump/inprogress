# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 11:42:27 2025

@author: lenny
"""

import pandas as pd
import matplotlib.pyplot as plt
import imageio.v3 as iio
import numpy as np

# ---------------- Parameter ----------------
INPUT_FILE = "matrix_strahlung_ueber_wasser.csv"
# INPUT_FILE = "matrix_strahlung_unter_wasser.csv" # Diese Zeile ein- und die vorige auskommentieren
                                                   # für Unterwassermatrix
INPUT_IMAGE_PNG = "flusslaufsbild.png"
VMIN = 0
VMAX = 1000 # für Unterwassermatrix auf 500 setzen
MARKERS = {"M1": 51, "M2": 191, "M3": 354, "M4": 452} # Segmente der Messstellen

# ---------------- CSV einlesen ----------------
df = pd.read_csv(INPUT_FILE, parse_dates=["time"])
time = df["time"]
matrix = df.drop(columns=["time"])
n_segments = matrix.shape[1]

# ---------------- PNG einlesen ----------------
img = iio.imread(INPUT_IMAGE_PNG)
img_h, img_w = img.shape[:2]

# ---------------- Figure & Axes ----------------
fig = plt.figure(figsize=(17, 11))
gs = fig.add_gridspec(2, 1, height_ratios=[4, 1], hspace=0.05)

ax_heat = fig.add_subplot(gs[0])
ax_img  = fig.add_subplot(gs[1], sharex=ax_heat)

# ---- Heatmap ----
im = ax_heat.imshow(
    matrix.values,
    aspect="auto",
    cmap="Reds",
    origin="upper",
    interpolation="nearest",
    vmin=VMIN,
    vmax=VMAX
)

# ---- Y-Achse Heatmap ----
time_rounded = time.dt.round("H")
mask_noon = (time_rounded.dt.hour == 12)
yticks = time_rounded[mask_noon].groupby(time_rounded.dt.date).head(1).index
yticklabels = [time.iloc[i].strftime("%d.%m") for i in yticks]
ax_heat.set_yticks(yticks)
ax_heat.set_yticklabels(yticklabels, fontsize=20)
ax_heat.set_ylabel("Zeit (MESZ, Markierung jeweils um 12:00 Uhr)", fontsize=22)

# ---- PNG unterhalb (Breite an Heatmap anpassen, Höhe proportional) ----
scale_png_width = 0.935  # 95 % der Heatmap-Breite
x0, y0, ax_width, ax_height = ax_heat.get_position().bounds

# PNG proportional skalieren
img_aspect = img_h / img_w
png_width = ax_width * scale_png_width
png_height = png_width * img_aspect

# Achse für PNG setzen (links fixiert bei x0)
ax_img.set_position([x0, ax_img.get_position().y0, png_width, ax_img.get_position().height])
ax_img.imshow(img, aspect='auto', extent=[0, n_segments-1, 0, png_height])
ax_img.axis('off')


# ---- Vertikale Markerlinien über beide Achsen ----
for pos in MARKERS.values():
    ax_heat.axvline(x=pos-1, color="blue", linestyle="--", linewidth=1.2)
    ax_img.axvline(x=pos-1, color="blue", linestyle="--", linewidth=1.2)
    ax_heat.text(pos-1, -5, [k for k,v in MARKERS.items() if v==pos][0],
                 ha='center', va='bottom', fontsize=20, fontweight="bold")

# ---- X-Achse nur am unteren Bild ----
xticks = list(range(0, n_segments, 50))
ax_img.set_xticks(xticks)
ax_img.set_xticklabels([str(x) for x in xticks], fontsize=20)
ax_img.set_xlabel("Flusssegmente", fontsize=26)

# ---- Farbleiste ----
cbar = fig.colorbar(im, ax=ax_heat, fraction=0.045, pad=0.02)
cbar.set_label("Strahlung (W m⁻²)", fontsize=26)
cbar.ax.tick_params(labelsize=20)

plt.show()



