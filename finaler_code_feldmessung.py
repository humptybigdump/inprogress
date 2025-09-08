# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 19:34:45 2025

@author: kopyf
"""


import os
import re
import argparse
import math
from datetime import time as dtime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


ORDNER = "."
OUTDIR = os.path.join(ORDNER, "finale_plots_parameter_feldmessung_zehrung")
os.makedirs(OUTDIR, exist_ok=True)

SMOOTH_MIN = 20
SMOOTH_METHOD = "mean"   
SMOOTH_FOR_FITS = True
GLOBAL_TRIM_MIN = 10

# Michaelis–Menten 
MM_C_FLOOR_DEFAULT = 0.15            # mg/L 
MM_KM_BOUNDS_DEFAULT = (0.05, 8.0)   # mg/L
MM_VMAX_BOUNDS_DEFAULT = (0.05/60, 8.0/60)  # mg L^-1 min^-1

# 0./1.-Ordnung
LIN_C_FLOOR_DEFAULT = MM_C_FLOOR_DEFAULT

# y-Achse
Y_MIN_DEFAULT = 0.0

# Farben
FARBEN = {
    "roh": "lightgray",
    "smooth": "black",
    "nullte": "tab:blue",
    "erste": "tab:orange",
    "mm": "tab:green",
}
MARKER_STYLE, MARKER_SIZE, MARKER_EDGEWIDTH = "x", 1.5, 0.1

# Messung 4: "Hügel" entfernen (20:00–00:00) 
M4_HUMP_START = dtime(20, 0)
M4_HUMP_END = dtime(0, 0)      
M4_HAMPEL_WIN = 31             # min für Median
M4_HAMPEL_SIGMA = 2.3          # Ausreißer-Schwelle
M4_FLOOR_MGL = 0.005           # untere Schranke 
M4_FRAC_RIGHT = 0.20           #  20% vom linken Wert

#  Mess-Abschnitte 
ABSCHNITTE = [
    (1, "2025-08-04 124000Z.txt", "2025-08-05 124200Z.txt", "Schlick",             None, 40),
    (2, "2025-08-06 145400Z.txt", "2025-08-07 145600Z.txt", "Schlick",             None, None),
    (3, "2025-08-10 092900Z.txt", "2025-08-09 092700Z.txt", "Schlick",             None, None),
    (4, "2025-08-11 123600Z.txt", "2025-08-10 123400Z.txt", "Schlick + Pflanze",   None, None),
    (5, "2025-08-12 144000Z.txt", "2025-08-11 143800Z.txt", "Schlick + Pflanze",   None, None),
    
    (6, "2025-08-14 162200Z.txt", "2025-08-13 162000Z.txt", "Pflanze",             None, None),  
    (7, "2025-08-14 164400Z.txt", None,                    "Pflanze",             None, None),  
    (8, "2025-08-15 164000Z.txt", "2025-08-16 164200Z.txt", "Kies",                None, None),  
    (9, "2025-08-16 173100Z.txt", None,                    "Kies",                None, None),  
]



# wichtig

def _find(path_or_name):
    """Sucht Datei im ORDNER (auch .txt fallback)."""
    if not path_or_name:
        return ""
    p = os.path.join(ORDNER, path_or_name)
    if os.path.exists(p):
        return p
    base, ext = os.path.splitext(path_or_name)
    if ext == "":
        p2 = os.path.join(ORDNER, base + ".txt")
        if os.path.exists(p2):
            return p2
    for f in os.listdir(ORDNER):
        if f == path_or_name or f == (base + ".txt"):
            return os.path.join(ORDNER, f)
    raise FileNotFoundError(f"Datei nicht gefunden: {path_or_name}")

def lade_und_bereinige(pfad):
    """CSV laden, plausible O2-Werte filtern, vorne/hinten trimmen, auf 1-min rastern + glätten."""
    df = pd.read_csv(
        pfad, skiprows=3, sep=",",
        names=["Time_sec", "BV", "Temp_C", "O2_mgL", "Q"],
        na_values=["", "NA", "NaN", " "]
    )
    df["Timestamp"] = pd.to_datetime(df["Time_sec"], unit="s", errors="coerce")
    df = df.dropna(subset=["Timestamp"]).set_index("Timestamp").sort_index()

    if "O2_mgL" in df.columns:
        df = df[(df["O2_mgL"] > 0) & (df["O2_mgL"] < 20)]

    if not df.empty:
        start = df.index.min() + pd.Timedelta(minutes=GLOBAL_TRIM_MIN)
        ende = df.index.max() - pd.Timedelta(minutes=GLOBAL_TRIM_MIN)
        df = df[(df.index >= start) & (df.index <= ende)]

    for c in ["O2_mgL", "Temp_C"]:
        if c in df.columns:
            df[c] = df[c].interpolate(limit=30)

    if not df.empty:
        idx = pd.date_range(df.index.min(), df.index.max(), freq="1min")
        df = df.reindex(idx)
        for c in ["O2_mgL", "Temp_C"]:
            if c in df.columns:
                df[c] = df[c].interpolate(method="time", limit_direction="both")

    if SMOOTH_MIN and SMOOTH_MIN > 0 and not df.empty:
        roll = df["O2_mgL"].rolling(f"{SMOOTH_MIN}min", center=True)
        smooth = roll.mean() if SMOOTH_METHOD == "mean" else roll.median()
        df["O2_smooth"] = smooth.fillna(df["O2_mgL"])
    else:
        df["O2_smooth"] = df.get("O2_mgL", pd.Series(index=df.index, dtype=float))

    return df

def info(nr, datei, data):
    print(f"[Info] Abschnitt {nr}, {os.path.basename(datei)}:")
    if not data.empty:
        print(f"  Zeitraum: {data.index.min()} → {data.index.max()} | Punkte: {len(data)}")
        print(f"  O2-Mittel: {data['O2_mgL'].mean():.3f} mg/L (min/max: {data['O2_mgL'].min():.2f}/{data['O2_mgL'].max():.2f})")
    else:
        print("  (leer nach Bereinigung)")
    print("-" * 60)

#  Zeitfenster  
def _time_window_mask(index, start_time, end_time):
    if start_time <= end_time:
        return index.map(lambda ts: start_time <= ts.time() <= end_time)
    return index.map(lambda ts: (ts.time() >= start_time) or (ts.time() <= end_time))

def _true_blocks(mask):
    blocks, on, s = [], False, None
    vals = mask.to_numpy()
    for i, v in enumerate(vals):
        if v and not on:
            on, s = True, i
        elif not v and on:
            blocks.append((s, i - 1)); on = False
    if on:
        blocks.append((s, len(vals) - 1))
    return blocks

# nur Messung 4
def despike_hampel_peakblock(df, col="O2_mgL",
                             start_time=M4_HUMP_START, end_time=M4_HUMP_END,
                             window_min=M4_HAMPEL_WIN, n_sigma=M4_HAMPEL_SIGMA):
    if df.empty or col not in df.columns:
        return df
    mask = _time_window_mask(df.index, start_time, end_time)
    blocks = _true_blocks(mask)
    if not blocks:
        return df
    # Block mit größtem Max 
    peak_idx, peak_val = None, -np.inf
    for i, j in blocks:
        vmax = float(np.nanmax(df[col].iloc[i:j+1].to_numpy()))
        if vmax > peak_val:
            peak_val, peak_idx = vmax, (i, j)
    i, j = peak_idx
    idx = df.index[i:j+1]

    s = df.loc[idx, col].copy()
    med = s.rolling(f"{window_min}min", center=True).median()
    abs_dev = (s - med).abs()
    mad = abs_dev.rolling(f"{window_min}min", center=True).median()
    sigma = 1.4826 * mad
    outliers = abs_dev > (n_sigma * sigma)
    s[outliers] = np.nan
    s = s.interpolate(method="time", limit_direction="both")

    df.loc[idx, col] = s
    return df

# Messung 4 (Ersatzkurve) 
def enforce_decay_peakblock(df, col="O2_mgL",
                            start_time=M4_HUMP_START, end_time=M4_HUMP_END,
                            floor=M4_FLOOR_MGL, frac_right=M4_FRAC_RIGHT):
    if df.empty or col not in df.columns:
        return df
    mask = _time_window_mask(df.index, start_time, end_time)
    blocks = _true_blocks(mask)
    if not blocks:
        return df
    peak_idx, peak_val = None, -np.inf
    for i, j in blocks:
        vmax = float(np.nanmax(df[col].iloc[i:j+1].to_numpy()))
        if vmax > peak_val:
            peak_val, peak_idx = vmax, (i, j)
    i, j = peak_idx
    idx_window = df.index[i:j+1]
    if len(idx_window) == 0:
        return df

    tL, tR = idx_window[0], idx_window[-1]
    left_slice = df.loc[(df.index < tL)].iloc[-10:]
    right_slice = df.loc[(df.index > tR)].iloc[:15]
    C_L = np.nanmedian(left_slice[col].to_numpy()) if not left_slice.empty else float(df[col].loc[tL])
    C_R_med = np.nanmedian(right_slice[col].to_numpy()) if not right_slice.empty else float(df[col].loc[tR])
    C_R_target = max(min(C_R_med, frac_right * C_L), floor)

    t_rel = (idx_window - tL).total_seconds() / 60.0
    T = t_rel[-1] if len(t_rel) else 0.0
    if T <= 0 or not np.isfinite(C_L) or C_L <= 0:
        y = np.linspace(C_L, C_R_target, len(idx_window))
    else:
        k = np.log((C_L + 1e-9) / (C_R_target + 1e-9)) / max(T, 1e-9)
        y = C_L * np.exp(-k * t_rel)

    y = np.minimum.accumulate(y)  
    y = np.clip(y, floor, C_L)
    df.loc[idx_window, col] = y
    return df

def re_smooth_inplace(df):
    if "O2_mgL" not in df.columns:
        return df
    if SMOOTH_MIN and SMOOTH_MIN > 0:
        roll = df["O2_mgL"].rolling(f"{SMOOTH_MIN}min", center=True)
        smooth = roll.mean() if SMOOTH_METHOD == "mean" else roll.median()
        df["O2_smooth"] = smooth.fillna(df["O2_mgL"])
    else:
        df["O2_smooth"] = df["O2_mgL"]
    return df

# Kinetiken 

def fit_zero_order_free(t_min, C):
    A = np.vstack([np.ones_like(t_min), t_min]).T
    a, b = np.linalg.lstsq(A, C, rcond=None)[0]
    k0 = -b
    return a, k0, a - k0 * t_min

def fit_first_order_free(t_min, C):
    Cpos = np.clip(C, 1e-9, None)
    y = np.log(Cpos)
    lnC0, k1 = np.linalg.lstsq(np.vstack([np.ones_like(t_min), -t_min]).T, y, rcond=None)[0]
    C0 = np.exp(lnC0)
    return C0, k1, C0 * np.exp(-k1 * t_min)

def fit_zero_order_anchored(t_min, C, C0, mask=None):
    t = t_min if mask is None else t_min[mask]
    y = C if mask is None else C[mask]
    if len(t) < 2 or np.allclose(np.sum(t**2), 0):
        return fit_zero_order_free(t_min, C)
    k0 = (np.sum(t * (C0 - y))) / np.sum(t**2)   # 1/min
    k0 = max(0.0, k0)
    pred = C0 - k0 * t_min
    return C0, k0, pred

def fit_first_order_anchored(t_min, C, C0, mask=None):
    Ceps = 1e-9
    t = t_min if mask is None else t_min[mask]
    y = np.log(np.clip(C if mask is None else C[mask], Ceps, None))
    if len(t) < 2 or np.allclose(np.sum(t**2), 0):
        return fit_first_order_free(t_min, C)
    lnC0 = np.log(max(C0, Ceps))
    k1 = (np.sum(t * (lnC0 - y))) / np.sum(t**2)  # 1/min
    k1 = max(0.0, k1)
    pred = C0 * np.exp(-k1 * t_min)
    return C0, k1, pred

def _mm_predict_series(t_min, C0, Vmax, Km):
    const = Km * np.log(C0) + C0
    Cpred = np.empty_like(t_min, float)
    for i, tt in enumerate(t_min):
        target = const - Vmax * tt
        x = max(C0 * np.exp(-Vmax * tt / max(Km, 1e-6)), 1e-6)
        for _ in range(80):
            fx = Km * np.log(max(x, 1e-12)) + x - target
            dfx = Km / max(x, 1e-12) + 1.0
            step = fx / dfx
            x -= step
            if abs(step) < 1e-9:
                break
            if x <= 0:
                x = 1e-6
        Cpred[i] = x
    return Cpred

def fit_mm_constrained(t_min, C, c_floor, km_bounds, vmax_bounds):
    mask = C > c_floor
    if mask.sum() < 5:
        mid = max(3, len(C)//2)
        mask = np.arange(len(C)) < mid
    t_fit = t_min[mask]
    y_fit = C[mask]
    C0 = float(y_fit[0])

    def err_of(V, K):
        Cp = _mm_predict_series(t_fit, C0, V, K)
        mse = np.nanmean((Cp - y_fit)**2)
        reg = 0.0
        min_k = max(0.08, km_bounds[0])
        if K < min_k:
            reg += (min_k - K)**2
        return mse + 0.05 * reg

    V_lo, V_hi = vmax_bounds
    K_lo, K_hi = km_bounds
    best = (np.inf, None, None)
    for V in np.logspace(np.log10(V_lo), np.log10(V_hi), 20):
        for K in np.logspace(np.log10(K_lo), np.log10(K_hi), 20):
            e = err_of(V, K)
            if e < best[0]:
                best = (e, V, K)
    err0, Vb, Kb = best

    def refine(Vc, Kc, fac=3.0, n=14):
        nonlocal err0, Vb, Kb
        V_vals = np.logspace(np.log10(max(V_lo, Vc/fac)), np.log10(min(V_hi, Vc*fac)), n)
        K_vals = np.logspace(np.log10(max(K_lo, Kc/fac)), np.log10(min(K_hi, Kc*fac)), n)
        for V in V_vals:
            for K in K_vals:
                e = err_of(V, K)
                if e < err0:
                    err0, Vb, Kb = e, V, K
    refine(Vb, Kb, fac=3.0, n=14)
    refine(Vb, Kb, fac=1.8, n=10)

    Cpred = _mm_predict_series(t_min, float(C[0]), Vb, Kb)
    return float(C[0]), Vb, Kb, Cpred

#  Standardfehler & RMSE 
def _se_reg_through_origin(x, y):
    if len(x) < 2:
        return float("nan")
    b = np.sum(x * y) / np.sum(x**2)
    resid = y - b * x
    dof = max(len(x) - 1, 1)
    s2 = float(np.sum(resid**2) / dof)
    var_b = s2 / float(np.sum(x**2))
    return math.sqrt(var_b)

def _mm_se_numeric(t_fit, y_fit, C0, V, K):
    def pred(v, k):
        return _mm_predict_series(t_fit, C0, v, k)
    r0 = pred(V, K) - y_fit
    rmse = math.sqrt(float(np.mean(r0**2)))
    n = len(t_fit); m = 2
    if n <= m:
        return float("nan"), float("nan"), rmse
    dV = (1e-6 + 1e-2 * abs(V))
    dK = (1e-6 + 1e-2 * abs(K))
    J = np.column_stack([
        (pred(V + dV, K) - pred(V, K)) / dV,
        (pred(V, K + dK) - pred(V, K)) / dK
    ])
    dof = max(n - m, 1)
    s2 = float(np.sum(r0**2) / dof)
    try:
        cov = s2 * np.linalg.inv(J.T @ J)
        se_V = float(np.sqrt(cov[0, 0]))
        se_K = float(np.sqrt(cov[1, 1]))
    except np.linalg.LinAlgError:
        se_V = se_K = float("nan")
    return se_V, se_K, rmse

#  Abschnitte verarbeiten

def verarbeite_abschnitt(nr, datei_a, datei_b, messtyp,
                         cut_bis=None, front_cut_total_min=None,
                         c_floor_mm=MM_C_FLOOR_DEFAULT,
                         km_bounds=MM_KM_BOUNDS_DEFAULT,
                         vmax_bounds=MM_VMAX_BOUNDS_DEFAULT,
                         anchor_c0=True, lin_c_floor=LIN_C_FLOOR_DEFAULT,
                         ymin=Y_MIN_DEFAULT):

    # Dateien laden
    pfade = []
    if datei_a: pfade.append(_find(datei_a))
    if datei_b: pfade.append(_find(datei_b))
    if not pfade:
        print(f"[{nr}] Keine Dateien – skip")
        return None

    dfs = []
    for p in pfade:
        d = lade_und_bereinige(p)

        # nur Messung 4: 
        if nr == 4 and not d.empty:
            d = despike_hampel_peakblock(d, col="O2_mgL",
                                         start_time=M4_HUMP_START, end_time=M4_HUMP_END,
                                         window_min=M4_HAMPEL_WIN, n_sigma=M4_HAMPEL_SIGMA)
            d = enforce_decay_peakblock(d, col="O2_mgL",
                                        start_time=M4_HUMP_START, end_time=M4_HUMP_END,
                                        floor=M4_FLOOR_MGL, frac_right=M4_FRAC_RIGHT)
            d = re_smooth_inplace(d)

        if cut_bis is not None and not d.empty:
            d = d[d.index.time <= cut_bis]
        info(nr, p, d)
        if not d.empty:
            d["_quelle"] = os.path.basename(p)
            dfs.append(d)

    if not dfs:
        print(f"[{nr}] Nach Bereinigung leer – skip")
        return None

    # Frontcut
    extra_front = 0
    if isinstance(front_cut_total_min, (int, float)):
        extra_front = max(0, int(front_cut_total_min) - GLOBAL_TRIM_MIN)

    # y-Achsen-Untergrenze (messung  4–8)
    bottom_lim = -1.0 if 4 <= nr <= 8 else ymin

    #  Rohplots 
    dfs_plot = dfs
    if extra_front > 0:
        all_start = min(d.index.min() for d in dfs)
        cut_start = all_start + pd.Timedelta(minutes=extra_front)
        tmp = []
        for d in dfs:
            dd = d[d.index >= cut_start]
            if cut_bis is not None:
                dd = dd[dd.index.time <= cut_bis]
            if not dd.empty:
                tmp.append(dd)
        dfs_plot = tmp if tmp else dfs

    fig, ax = plt.subplots(figsize=(11, 5.8))
    for d in dfs_plot:
        ax.plot(d.index, d["O2_mgL"], "-", color=FARBEN["roh"], alpha=0.65, label=f"{d['_quelle'].iloc[0]} roh")
        ax.plot(d.index, d["O2_smooth"], "-", color=FARBEN["smooth"], label=f"{d['_quelle'].iloc[0]} glätt.")
    ax.set_title(f"Zehrungsplot – Messung {nr} ({messtyp})")
    ax.set_xlabel("Uhrzeit"); ax.set_ylabel("Gelöster Sauerstoff [mg/L]")
    ax.grid(True); ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    if bottom_lim is not None:
        ax.set_ylim(bottom=bottom_lim)
    fig.autofmt_xdate(); ax.legend(ncols=2)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTDIR, f"m{nr:02d}_roh.png"), dpi=200)
    plt.close(fig)

    # Fits 
    d_all = pd.concat([d[["O2_mgL", "O2_smooth", "Temp_C"]] for d in dfs if not d.empty]).sort_index()
    d_all = d_all[~d_all.index.duplicated(keep="first")]

    if extra_front > 0 and not d_all.empty:
        fit_start = d_all.index.min() + pd.Timedelta(minutes=extra_front)
        d_all = d_all[d_all.index >= fit_start]
    if cut_bis is not None and not d_all.empty:
        d_all = d_all[d_all.index.time <= cut_bis]
    if d_all.empty:
        print(f"[{nr}] Keine Daten für Fits – skip")
        return None

    full_index = pd.date_range(d_all.index.min(), d_all.index.max(), freq="1min")
    d_full = d_all.reindex(full_index)
    for col in ["O2_mgL", "O2_smooth", "Temp_C"]:
        if col in d_full.columns:
            d_full[col] = d_full[col].interpolate(method="time", limit_direction="both")
    if d_full.empty or d_full["O2_smooth"].isna().all():
        print(f"[{nr}] Keine Daten für Fits – skip")
        return None

    t0 = d_full.index.min()
    t_min = (d_full.index - t0).total_seconds() / 60.0
    y = d_full["O2_smooth" if SMOOTH_FOR_FITS else "O2_mgL"].to_numpy()

    C0_anchor = float(y[0])
    mask_lin = y > max(1e-6, lin_c_floor)

    t_lin = t_min[mask_lin]
    y_lin = y[mask_lin]

    # 0. Ordnung 
    _, k0_min, C0p = fit_zero_order_anchored(t_min, y, C0_anchor, mask=mask_lin)  # 1/min
    se_k0_min = _se_reg_through_origin(t_lin, (C0_anchor - y_lin))
    rmse0 = math.sqrt(float(np.mean((C0_anchor - k0_min * t_lin - y_lin)**2)))

    # 1. Ordnung 
    _, k1_min, C1p = fit_first_order_anchored(t_min, y, C0_anchor, mask=mask_lin)  # 1/min
    Ceps = 1e-9
    ylog_lin = np.log(np.clip(y_lin, Ceps, None))
    se_k1_min = _se_reg_through_origin(t_lin, (np.log(max(C0_anchor, Ceps)) - ylog_lin))
    rmse1 = math.sqrt(float(np.mean((C0_anchor * np.exp(-k1_min * t_lin) - y_lin)**2)))

    # Michaelis–Menten 
    _, Vmin, Km, CMp = fit_mm_constrained(
        t_min, y, c_floor=c_floor_mm, km_bounds=km_bounds, vmax_bounds=vmax_bounds
    )

    mask_mm = y > c_floor_mm
    if mask_mm.sum() < 5:
        mid = max(3, len(y)//2)
        mask_mm = np.arange(len(y)) < mid
    t_mm = t_min[mask_mm]
    y_mm = y[mask_mm]
    C0_mm = float(y_mm[0])
    se_Vmin, se_Km, rmse_mm = _mm_se_numeric(t_mm, y_mm, C0_mm, Vmin, Km)

    #  Plot Modelle
    fig2, ax2 = plt.subplots(figsize=(9.2, 6.0))
    ax2.plot(d_full.index, y, linestyle="None", marker=MARKER_STYLE, color=FARBEN["smooth"],
             markersize=MARKER_SIZE, markeredgewidth=MARKER_EDGEWIDTH,
             label="Messwerte (glätt.)" if SMOOTH_FOR_FITS else "Messwerte")
    ax2.plot(d_full.index, C0p, "--", label="Nullte Ordnung", color=FARBEN["nullte"])
    ax2.plot(d_full.index, C1p, ":", label="Erste Ordnung", color=FARBEN["erste"])
    ax2.plot(d_full.index, CMp, "-", label="Michaelis–Menten", color=FARBEN["mm"])
    ax2.set_title(f"Zehrungsplot – Messung {nr} ({messtyp})")
    ax2.set_xlabel("Uhrzeit"); ax2.set_ylabel("Gelöster Sauerstoff [mg/L]")
    ax2.grid(True); ax2.legend()
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    if bottom_lim is not None:
        ax2.set_ylim(bottom=bottom_lim)
    fig2.autofmt_xdate()
    txt = (f"Nullte Ordnung: k₀ = {k0_min*60:.3f} mg L⁻¹ h⁻¹\n"
           f"Erste Ordnung: k₁ = {k1_min*60:.3f} h⁻¹\n"
           f"Michaelis–Menten: Vmax = {Vmin*60:.3f} mg L⁻¹ h⁻¹, Km = {Km:.3f} mg L⁻¹")
    ax2.text(0.02, 0.03, txt, transform=ax2.transAxes, fontsize=9,
             bbox=dict(boxstyle="round", alpha=0.12))
    plt.tight_layout()
    fig2.savefig(os.path.join(OUTDIR, f"m{nr:02d}_modelle.png"), dpi=200)
    plt.close(fig2)

    #  Parameter (h^-1 & mg/L/h)
    row = {
        "Messung": nr,
        "Typ": messtyp,
        "k0 (mg/L h^-1)": k0_min * 60.0,
        "k0_se": se_k0_min * 60.0,
        "RMSE0 (mg/L)": rmse0,
        "k1 (h^-1)": k1_min * 60.0,
        "k1_se": se_k1_min * 60.0,
        "RMSE1 (mg/L)": rmse1,
        "Vmax (mg/L h^-1)": Vmin * 60.0,
        "Vmax_se": se_Vmin * 60.0,
        "Km (mg/L)": Km,
        "Km_se": se_Km,
        "RMSE_MM (mg/L)": rmse_mm,
    }

    print(f"[{nr}] Parameter: k0={row['k0 (mg/L h^-1)']:.3f}±{row['k0_se']:.3f}, "
          f"k1={row['k1 (h^-1)']:.3f}±{row['k1_se']:.3f}, "
          f"Vmax={row['Vmax (mg/L h^-1)']:.3f}±{row['Vmax_se']:.3f}, Km={row['Km (mg/L)']:.3f}±{row['Km_se']:.3f}")
    return row

#  Unsicherheiten 
def _pm(v, se):
    return "—" if (np.isnan(v) or np.isnan(se)) else f"{v:.3f} ± {se:.3f}"

def parse_weights(s):
    """'Schlick=0.3,Pflanze=0.5,Kies=0.2' -> dict, auf Summe 1 normiert"""
    w = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        k, v = part.split("=")
        w[k.strip()] = float(v)
    tot = sum(w.values())
    if tot > 0:
        for k in list(w.keys()):
            w[k] = w[k] / tot
    return w

def group_uncertainties(df, param_col, se_col, group_col="Typ"):
    rows = []
    for g, dfg in df.groupby(group_col, dropna=False):
        r = dfg[param_col].dropna().to_numpy()
        s = dfg[se_col].dropna().to_numpy()
        n = len(r)
        if n == 0:
            rows.append({"Gruppe": g, "n": 0, "Mittel": np.nan, "Sigma": np.nan})
            continue
        rbar = float(np.mean(r))
        term1 = float(np.mean(s**2)) if s.size else 0.0
        term2 = float(np.sum((r - rbar)**2) / max(n - 1, 1))
        sigma = math.sqrt(term1 + term2)
        rows.append({"Gruppe": g, "n": n, "Mittel": rbar, "Sigma": sigma})
    return pd.DataFrame(rows)

def combine_uncertainty(sigmas, weights, hA):
    num = 0.0
    for g, f in weights.items():
        if g in sigmas and np.isfinite(sigmas[g]):
            num += f * (sigmas[g]**2)
    if hA <= 0:
        hA = 1.0
    return math.sqrt(num / hA) if num > 0 else float("nan")

def _safe_name(s):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)

# wichtig
def _parse_args():
    p = argparse.ArgumentParser(description="Ammer Zehrung – Plots + Parameter + RMSE + Unsicherheiten (1–9)")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=9)
    p.add_argument("--only", type=int, nargs="+")
    p.add_argument("--c_floor", type=float, default=MM_C_FLOOR_DEFAULT)
    p.add_argument("--km_min", type=float, default=MM_KM_BOUNDS_DEFAULT[0])
    p.add_argument("--km_max", type=float, default=MM_KM_BOUNDS_DEFAULT[1])
    p.add_argument("--vmax_min", type=float, default=MM_VMAX_BOUNDS_DEFAULT[0]*60)
    p.add_argument("--vmax_max", type=float, default=MM_VMAX_BOUNDS_DEFAULT[1]*60)
    p.add_argument("--no_anchor", action="store_true")
    p.add_argument("--lin_c_floor", type=float, default=LIN_C_FLOOR_DEFAULT)
    p.add_argument("--ymin", type=float, default=Y_MIN_DEFAULT, help="untere y-Achsen-Grenze (Default 0.0)")

    #  kombinierte Unsicherheit
    p.add_argument("--weights", type=str, default="", help="Gewichte f_i je Gruppe, z.B. 'Schlick=0.4,Pflanze=0.4,Kies=0.2'")
    p.add_argument("--hA", type=float, default=1.0, help="mittlere Wassertiefe h_A (Skalierung), Default 1.0")
    return p.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    c_floor_mm = float(args.c_floor)
    km_bounds = (float(args.km_min), float(args.km_max))
    vmax_bounds = (float(args.vmax_min)/60.0, float(args.vmax_max)/60.0)
    anchor_c0 = not args.no_anchor  
    lin_c_floor = float(args.lin_c_floor)
    ymin = float(args.ymin)
    weights = parse_weights(args.weights) if args.weights else {}

    if args.only:
        auswahl = [t for t in ABSCHNITTE if t[0] in set(args.only)]
        auswahl.sort(key=lambda x: x[0])
        print(f"Laufe NUR Abschnitte: {[t[0] for t in auswahl]}")
    else:
        auswahl = [t for t in ABSCHNITTE if args.start <= t[0] <= args.end]
        print(f"Laufe Abschnitte {args.start}–{args.end} → {[t[0] for t in auswahl]}")

    rows = []
    for nr, a, b, typ, cut, front in auswahl:
        try:
            r = verarbeite_abschnitt(
                nr, a, b, typ,
                cut_bis=cut,
                front_cut_total_min=front,
                c_floor_mm=c_floor_mm,
                km_bounds=km_bounds,
                vmax_bounds=vmax_bounds,
                anchor_c0=anchor_c0,
                lin_c_floor=lin_c_floor,
                ymin=ymin
            )
            if r is not None:
                rows.append(r)
        except FileNotFoundError as e:
            print(f"[{nr}] FEHLER: {e} – Abschnitt übersprungen.")
        except Exception as e:
            print(f"[{nr}] Unerwarteter Fehler: {e} – Abschnitt übersprungen.")

    if not rows:
        print("\nKeine Parameter berechnet (keine passenden Abschnitte).")
        raise SystemExit

    df = pd.DataFrame(rows).sort_values("Messung")
    df.to_csv(os.path.join(OUTDIR, "parameter_robust.csv"), index=False)

    # Tabelle  CSV 
    def _pm_tex_like(v, se):
        return "—" if (np.isnan(v) or np.isnan(se)) else f"{v:.3f} ± {se:.3f}"

    def _find_col(prefix):
        for c in df.columns:
            if c.startswith(prefix):
                return c
        raise KeyError(f"Spalte mit Präfix '{prefix}' nicht gefunden")

    RMSE0_COL = _find_col("RMSE0") if any(c.startswith("RMSE0") for c in df.columns) else _find_col("RMSE_0")
    RMSE1_COL = _find_col("RMSE1") if any(c.startswith("RMSE1") for c in df.columns) else _find_col("RMSE_1")
    RMSEMM_COL = _find_col("RMSE_MM")

    pretty = pd.DataFrame({
        "Messung": df["Messung"],
        "Untergrund": df["Typ"],
        "$k_0$ [mg L$^{-1}$ h$^{-1}$]": [_pm_tex_like(v, s) for v, s in zip(df["k0 (mg/L h^-1)"], df["k0_se"])],
        "RMSE$_0$ [mg L$^{-1}$]": df[RMSE0_COL].map(lambda x: f"{x:.3f}"),
        "$k_1$ [h$^{-1}$]": [_pm_tex_like(v, s) for v, s in zip(df["k1 (h^-1)"], df["k1_se"])],
        "RMSE$_1$ [mg L$^{-1}$]": df[RMSE1_COL].map(lambda x: f"{x:.3f}"),
        "$V_{\\max}$ [mg L$^{-1}$ h$^{-1}$]": [_pm_tex_like(v, s) for v, s in zip(df["Vmax (mg/L h^-1)"], df["Vmax_se"])],
        "$K_M$ [mg L$^{-1}$]": [_pm_tex_like(v, s) for v, s in zip(df["Km (mg/L)"], df["Km_se"])],
        "RMSE$_{\\mathrm{MM}}$ [mg L$^{-1}$]": df[RMSEMM_COL].map(lambda x: f"{x:.3f}"),
    })

    # CSV ausgeben 
    pretty.to_csv(os.path.join(OUTDIR, "parameter_table_pretty.csv"), index=False)
    print(f"\nGespeichert → {os.path.join(OUTDIR, 'parameter_robust.csv')}")
    print(f"Gespeichert → {os.path.join(OUTDIR, 'parameter_table_pretty.csv')}")

    #  Unsicherheiten je Untergrund 
    tables = {}
    for (param, se) in [
        ("k0 (mg/L h^-1)", "k0_se"),
        ("k1 (h^-1)", "k1_se"),
        ("Vmax (mg/L h^-1)", "Vmax_se"),
        ("Km (mg/L)", "Km_se"),
    ]:
        tab = group_uncertainties(df, param, se, group_col="Typ")
        tables[param] = tab

        csv_path = os.path.join(OUTDIR, f"uncert_{_safe_name(param)}.csv")
        tab.to_csv(csv_path, index=False)
        print(f"Gespeichert → {csv_path}")

    #  Kombinierte Unsicherheit 
    if weights:
        summary_lines = []
        for (param, _) in [
            ("k0 (mg/L h^-1)", "k0_se"),
            ("k1 (h^-1)", "k1_se"),
            ("Vmax (mg/L h^-1)", "Vmax_se"),
            ("Km (mg/L)", "Km_se"),
        ]:
            tab = tables[param]
            sigmas = {row["Gruppe"]: row["Sigma"] for _, row in tab.iterrows()}
            sigma_comb = combine_uncertainty(sigmas, weights, args.hA)
            summary_lines.append(f"{param}: sigma_total = {sigma_comb:.4f} (Gewichte={weights}, h_A={args.hA})")
        with open(os.path.join(OUTDIR, "uncertainty_combined.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(summary_lines))
        print("\nGesamt-Unsicherheiten:")
        for line in summary_lines:
            print("  " + line)
    else:
        print("\nHinweis: Für kombinierte Unsicherheit Gewichte angeben, z.B.:")
        print("  --weights 'Schlick=0.4,Pflanze=0.4,Kies=0.2' --hA 1.2")
