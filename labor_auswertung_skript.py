#!/usr/bin/env python3
"""
Auswertung Labor-Zehrung

Pipeline:
1) Daten einlesen (Schlick, Steine, Pflanzen; inkl. Blanks)
2) Ausreißer entfernen (einfacher linearer Check)
3) Fits: Nullte Ordnung, Erste Ordnung, Michaelis–Menten
4) Plots (inkl. Sammelplot für Blanks)
5) Parameter + RMSE in CSV und LaTeX exportieren

Hinweis:
- Zeit wird in Minuten eingelesen, intern bei Fits aber oft auf Stunden umgerechnet.
- Michaelis–Menten (MM) wird mit kleiner Multistart-Suche und robustem Loss gefittet.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, Tuple, Optional, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit, least_squares

# Ausreißer-Schwelle (σ um eine lineare Trendlinie). 2.0 ist „leicht robust“.
THRESH_SIGMA: float = 2.0

# Suchbereich für Michaelis–Menten-Parameter (Vmax [mg L^-1 h^-1], Km [mg L^-1])
MM_BOUNDS: Dict[str, float] = {
    "Vmax_min": 1e-4,
    "Vmax_max": 10.0,
    "Km_min": 1e-3,
    "Km_max": 20.0,
}

# Plausibilitäts-Checks für MM (damit keine grenzwertigen/unsinnigen Lösungen stehen bleiben)
PLAUS_CUTOFFS: Dict[str, float] = {
    "Vmax_max": 20.0,   # sehr großzügige Obergrenze
    "Km_max": 50.0,
    "rmse_factor": 1.2, # MM darf nicht deutlich schlechter sein als beste lineare Alternative
}

#I/O-Helfer 

def clean_numeric_cols(df: pd.DataFrame, time_col: int, o2_col: int) -> Tuple[np.ndarray, np.ndarray]:
    """Zieht Zeit (min) und O2 (mg/L) aus Spalten, wirft NaNs raus, sortiert nach Zeit."""
    t = pd.to_numeric(df.iloc[:, time_col], errors="coerce")
    c = pd.to_numeric(df.iloc[:, o2_col], errors="coerce")
    m = t.notna() & c.notna()
    t = t[m].astype(float).to_numpy()
    c = c[m].astype(float).to_numpy()
    order = np.argsort(t)
    return t[order], c[order]

def _guess_time_o2_from_sheet(df: pd.DataFrame) -> Optional[Tuple[np.ndarray, np.ndarray, int, int]]:
    """
    Heuristik: findet ein plausibles (Zeit, O2)-Spaltenpaar im Sheet.
    Idee: viele Punkte, Zeit überwiegend monoton steigend, O2 grob in [0, 30] mg/L.
    """
    best = None
    ncols = df.shape[1]
    for i in range(ncols):
        for j in range(ncols):
            if i == j:
                continue
            try:
                t, c = clean_numeric_cols(df, i, j)
            except Exception:
                continue
            if t.size < 3:
                continue
            diffs = np.diff(t)
            mono_ratio = (diffs > 0).sum() / max(len(diffs), 1)
            c_ok = float((c >= 0).mean() * (c <= 30).mean())
            score = t.size + 5.0 * mono_ratio + 3.0 * c_ok
            if (best is None) or (score > best[0]):
                best = (score, t, c, i, j)
    if best is None:
        return None
    _, t, c, ti, ci = best
    if (np.diff(t) > 0).mean() < 0.6:
        return None
    return t, c, ti, ci

def read_last_sheet_pair(xlsx_path: str, known_primary_sheet: str = "Tabelle1"
                         ) -> Optional[Tuple[str, np.ndarray, np.ndarray]]:
    """
    Für Pflanzen-Excel: liest das letzte Blatt, sofern es NICHT das bekannte Standardblatt ist.
    Praktisch, wenn man später noch ein neues Blatt angehängt hat.
    """
    xf = pd.ExcelFile(xlsx_path)
    if not xf.sheet_names:
        return None
    last_name = xf.sheet_names[-1]
    if last_name.strip() == known_primary_sheet.strip():
        return None
    df_last = pd.read_excel(xlsx_path, sheet_name=last_name, header=None)
    guessed = _guess_time_o2_from_sheet(df_last)
    if guessed is None:
        print(f"[Hinweis] Letztes Blatt '{last_name}': keine passenden Spalten gefunden.")
        return None
    t, c, ti, ci = guessed
    print(f"[Info] Neues Blatt: '{last_name}' (Zeit-Spalte {ti}, O2-Spalte {ci}); Punkte: {len(t)}")
    return last_name, t, c

def read_last_sheet_pair_excluding(xlsx_path: str, exclude_names: List[str]
                                   ) -> Optional[Tuple[str, np.ndarray, np.ndarray]]:
    """
    Für Schlick/Steine-Excel: liest das letzte Blatt, wenn es NICHT in exclude_names steckt.
    Damit greifen wir automatisch neue Blätter auf.
    """
    xf = pd.ExcelFile(xlsx_path)
    if not xf.sheet_names:
        return None
    last_name = xf.sheet_names[-1]
    if last_name.strip() in {n.strip() for n in exclude_names}:
        return None
    df_last = pd.read_excel(xlsx_path, sheet_name=last_name, header=None)
    guessed = _guess_time_o2_from_sheet(df_last)
    if guessed is None:
        print(f"[Hinweis] Letztes Blatt '{last_name}': keine passenden Spalten gefunden.")
        return None
    t, c, ti, ci = guessed
    print(f"[Info] Zusatzblatt: '{last_name}' (Zeit-Spalte {ti}, O2-Spalte {ci}); Punkte: {len(t)}")
    return last_name, t, c

#Ausreißer 

def remove_outliers_linear(t: np.ndarray, c: np.ndarray, thresh_sigma: float = THRESH_SIGMA
                           ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Einfacher Filter: lineare Regression C ~ a + b t, Residuen per σ normieren,
    Punkte mit |resid| > thresh*σ fliegen raus.
    """
    A = np.vstack([np.ones_like(t), t]).T
    params, *_ = np.linalg.lstsq(A, c, rcond=None)
    resid = c - (A @ params)
    sigma = np.std(resid, ddof=1) if resid.size > 1 else 0.0
    keep = np.ones_like(c, dtype=bool) if sigma == 0 else (np.abs(resid) <= thresh_sigma * sigma)
    return t[keep], c[keep], keep

# Modelle / Fits

def fit_zero_order(t_min: np.ndarray, c: np.ndarray) -> Tuple[Dict[str, float], np.ndarray, np.ndarray]:
    """
    Nullte Ordnung: C(t) = C0 - k0 * t
    - Eingabezeit t_min in Minuten -> intern in Stunden umgerechnet
    - k0 in mg L^-1 h^-1
    """
    t_h = np.asarray(t_min, float) / 60.0
    A = np.vstack([np.ones_like(t_h), t_h]).T
    C0, slope_h = np.linalg.lstsq(A, c, rcond=None)[0]
    k0_h = -slope_h
    C_fit = C0 - k0_h * t_h
    return {"C0": float(C0), "k0": float(k0_h)}, t_min, C_fit

def fit_first_order(t_min: np.ndarray, c: np.ndarray) -> Tuple[Dict[str, float], np.ndarray, np.ndarray]:
    """
    Erste Ordnung: C(t) = C0 * exp(-k1 * t)
    - t in h, k1 in h^-1
    - Startwerte aus Log-Differenz grob geraten
    """
    t_h = np.asarray(t_min, float) / 60.0

    def model(th, C0, k1):
        return C0 * np.exp(-k1 * th)

    C0g = max(c[0], 1e-9)
    k1g = max(1e-9, (np.log(C0g) - np.log(max(c[-1], 1e-9))) / max(t_h[-1] - t_h[0], 1e-9))
    C0, k1 = curve_fit(model, t_h, c, p0=[C0g, k1g], bounds=(0, np.inf), maxfev=50_000)[0]
    C_fit = model(t_h, C0, k1)
    return {"C0": float(C0), "k1": float(k1)}, t_min, C_fit

def solve_mm_per_hour(t_min: np.ndarray, C0: float, Vmax_h: float, Km: float) -> np.ndarray:
    """
    MM-DGL: dC/dt = - Vmax * C / (Km + C)
    - Integration mit solve_ivp auf t in MINUTEN
    - Vmax kommt in mg L^-1 h^-1 rein, wird auf pro Minute umgerechnet
    """
    Vmin = Vmax_h / 60.0

    def rhs(_, C):
        return -Vmin * C / (Km + C)

    sol = solve_ivp(rhs, (float(t_min[0]), float(t_min[-1])), [float(C0)],
                    t_eval=t_min, rtol=1e-8, atol=1e-10)
    return sol.y[0]

def fit_mm(t_min: np.ndarray, c: np.ndarray
           ) -> Tuple[Dict[str, float], np.ndarray, np.ndarray]:
    """
    Michaelis–Menten-Fit:
    - kleine Multistart-Suche über Vmax und Km
    - robustes Loss (soft_l1), enge Bounds
    - gibt auch Flag zurück, falls Lösung „an Grenze“ liegt
    """
    t_min = np.asarray(t_min, float)
    c = np.asarray(c, float)
    C0g = float(c[0])

    V_starts = np.array([0.2, 0.5, 1.0, 2.0, 5.0])          # mg L^-1 h^-1
    Km_starts = np.array([0.5, 1.0, 2.0, 5.0, 10.0, 15.0])  # mg L^-1

    lower = [0.0, MM_BOUNDS["Vmax_min"], MM_BOUNDS["Km_min"]]
    upper = [np.inf, MM_BOUNDS["Vmax_max"], MM_BOUNDS["Km_max"]]

    def residuals(p: np.ndarray) -> np.ndarray:
        C0, Vh, Km = p
        return solve_mm_per_hour(t_min, abs(C0), abs(Vh), max(abs(Km), 1e-12)) - c

    best_res, best_err = None, None
    for V0 in V_starts:
        for K0 in Km_starts:
            p0 = np.array([C0g, V0, K0], dtype=float)
            res = least_squares(residuals, x0=p0, bounds=(lower, upper),
                                loss="soft_l1", f_scale=0.1, max_nfev=5_000)
            err = float(np.mean(res.fun**2))
            if best_err is None or err < best_err:
                best_err, best_res = err, res

    C0, Vmax_h, Km = best_res.x
    C_fit = solve_mm_per_hour(t_min, C0, Vmax_h, Km)

    # Flag: liegt die Lösung genau an den Bounds?
    tol = 0.01
    at_lower = (abs(Vmax_h - MM_BOUNDS["Vmax_min"]) <= tol*max(1.0, MM_BOUNDS["Vmax_min"])
                or abs(Km - MM_BOUNDS["Km_min"]) <= tol*max(1.0, MM_BOUNDS["Km_min"]))
    at_upper = (abs(Vmax_h - MM_BOUNDS["Vmax_max"]) <= tol*MM_BOUNDS["Vmax_max"]
                or abs(Km - MM_BOUNDS["Km_max"]) <= tol*MM_BOUNDS["Km_max"])

    return {"C0": float(C0), "Vmax": float(Vmax_h), "Km": float(Km),
            "bound_hit": bool(at_lower or at_upper)}, t_min, C_fit

# Plots 
def plot_with_fits(title: str, t: np.ndarray, c: np.ndarray) -> None:
    """
    Ein Plot pro Probe:
    - Rohdaten
    - Ausreißer (falls vorhanden, grau)
    - Fits (0., 1., MM) mit Legende inkl. Hauptparametern
    """
    plt.figure(figsize=(6, 4.5), dpi=140)
    plt.plot(t, c, linestyle="None", marker="x", color="blue", label="Rohdaten")

    # Ausreißer markieren
    t_clean, c_clean, keep = remove_outliers_linear(t, c, THRESH_SIGMA)
    if keep.sum() < keep.size:
        out_t, out_c = t[~keep], c[~keep]
        if out_t.size:
            plt.plot(out_t, out_c, linestyle="None", marker="o", color="gray", label="Ausreißer")

    # Fits
    p0, tz, cz = fit_zero_order(t_clean, c_clean)
    p1, t1, c1 = fit_first_order(t_clean, c_clean)
    pmm, tm, cm = fit_mm(t_clean, c_clean)

    plt.plot(tz, cz, color="black", linewidth=2.0,
             label=f"Nullte Ordnung (k0={p0['k0']:.3g} mg L$^{{-1}}$ h$^{{-1}}$)")
    plt.plot(t1, c1, color="green", linewidth=2.0, linestyle="--",
             label=f"Erste Ordnung (k1={p1['k1']:.3g} h$^{{-1}}$)")
    suffix = " (an Grenze)" if pmm["bound_hit"] else ""
    plt.plot(tm, cm, color="red", linewidth=2.0, linestyle=":",
             label=f"MM (Vmax={pmm['Vmax']:.3g} mg L$^{{-1}}$ h$^{{-1}}$, Km={pmm['Km']:.3g} mg L$^{{-1}}$){suffix}")

    plt.xlabel("Zeit [min]")
    plt.ylabel("Gelöster Sauerstoff [mg L$^{-1}$]")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend(loc="best", framealpha=1.0, fontsize=7)
    plt.tight_layout()
    plt.show()

def plot_blanks(t_sb: np.ndarray, c_sb: np.ndarray,
                t_stb: np.ndarray, c_stb: np.ndarray,
                t_pb: np.ndarray, c_pb: np.ndarray) -> None:
    """Sammelplot für die drei Blank-Reihen (Schlick/Steine/Pflanzen)."""
    plt.figure(figsize=(6, 4.5), dpi=140)
    plt.plot(t_sb, c_sb, "x-", label="Blank Schlick")
    plt.plot(t_stb, c_stb, "s-", label="Blank Steine")
    plt.plot(t_pb, c_pb, "^-", label="Blank Pflanzen")
    plt.xlabel("Zeit [min]")
    plt.ylabel("Gelöster Sauerstoff [mg L$^{-1}$]")
    plt.title("Blanks: Sauerstoffabnahme (Referenzwasser)")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.show()

#Statistik/Tabellen 

def _linreg_se(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Lineare Regression y = a + b x
    Rückgabe:
      - beta = (a, b)
      - se = Standardfehler von (a, b)
      - rmse im y-Raum
    """
    X = np.vstack([np.ones_like(x), x]).T
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - (X @ beta)
    n, p = X.shape
    s2 = float(np.sum(resid**2) / max(n - p, 1))
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    rmse = math.sqrt(float(np.mean(resid**2)))
    return beta, se, rmse

def _mm_cov_from_jac(residual_fun: Callable[[np.ndarray], np.ndarray],
                     p_opt: np.ndarray) -> np.ndarray:
    """
    Kovarianzabschätzung ~ s^2 * (J^T J)^-1 am Optimum.
    J wird numerisch per Vorwärtsdifferenzen genähert.
    """
    eps = np.sqrt(np.finfo(float).eps)
    p = np.asarray(p_opt, float)
    f0 = residual_fun(p)
    n, m = f0.size, p.size
    J = np.zeros((n, m))
    for j in range(m):
        dp = np.zeros_like(p); dp[j] = eps * (abs(p[j]) + 1.0)
        J[:, j] = (residual_fun(p + dp) - f0) / dp[j]
    dof = max(n - m, 1)
    s2 = float(np.sum(f0**2) / dof)
    try:
        return s2 * np.linalg.inv(J.T @ J)
    except np.linalg.LinAlgError:
        return np.full((m, m), np.nan)

def _plausibility_mask(vmax: float, km: float, rmse_mm: float,
                       rmse0: float, rmse1: float, at_bound: bool) -> Tuple[bool, str]:
    """
    Prüft grobe Plausibilität der MM-Ergebnisse.
    ok = True, wenn alles im Rahmen; sonst False + kurzer Grund.
    """
    reasons = []
    if vmax > PLAUS_CUTOFFS["Vmax_max"]:
        reasons.append(f"Vmax>{PLAUS_CUTOFFS['Vmax_max']}")
    if km > PLAUS_CUTOFFS["Km_max"]:
        reasons.append(f"Km>{PLAUS_CUTOFFS['Km_max']}")
    best_linear = min(rmse0, rmse1)
    if rmse_mm > PLAUS_CUTOFFS["rmse_factor"] * best_linear:
        reasons.append("RMSE schlecht")
    if at_bound:
        reasons.append("an Grenze")
    return (len(reasons) == 0), ", ".join(reasons)

def compute_parameters_for_series(label: str, t: np.ndarray, c: np.ndarray) -> Dict[str, float | str]:
    """
    Komplettpaket für eine Probe:
    - Ausreißer filtern
    - 0. Ordnung fitten (m = k0)
    - 1. Ordnung fitten (k1), RMSE im Konzentrationsraum
    - MM fitten, Plausibilität checken, ggf. SE über numerische Jacobimatrix
    - alles als Dict zurück
    """
    # Ausreißer entfernen (linearer Quick-Check)
    t_c, c_c, _ = remove_outliers_linear(t, c, THRESH_SIGMA)
    if t_c.size < 3:
        raise ValueError(f"Zu wenige Punkte nach Ausreißerfilter für {label}")

    # Nullte Ordnung: Regression im Konzentrationsraum
    t_h = t_c / 60.0
    (a0, b0), (se_a0, se_b0), rmse0 = _linreg_se(t_h, c_c)
    m_val, m_se = -b0, se_b0  # Steigung negativ => Rate ist -b

    # Erste Ordnung: Linearisiert via log(C); RMSE wieder im Konzentrationsraum
    Cpos = np.clip(c_c, 1e-9, None)
    ylog = np.log(Cpos)
    (A1, B1), (se_A1, se_B1), _ = _linreg_se(t_h, ylog)
    k1_val, k1_se = -B1, se_B1
    rmse1 = math.sqrt(float(np.mean((np.exp(A1 + B1 * t_h) - c_c) ** 2)))

    # MM fitten
    pmm, _, Cmm = fit_mm(t_c, c_c)
    vmax_h, km_val, at_bound = pmm["Vmax"], pmm["Km"], pmm["bound_hit"]
    rmse_mm = math.sqrt(float(np.mean((Cmm - c_c) ** 2)))

    # Plausibilität
    ok, reason = _plausibility_mask(vmax_h, km_val, rmse_mm, rmse0, rmse1, at_bound)
    if ok:
        def resid_mm(p: np.ndarray) -> np.ndarray:
            C0, Vh, Km = p
            return solve_mm_per_hour(t_c, C0, Vh, Km) - c_c
        cov = _mm_cov_from_jac(resid_mm, np.array([float(c_c[0]), vmax_h, km_val], float))
        se_vmax = float(np.sqrt(cov[1, 1])) if np.isfinite(cov[1, 1]) else np.nan
        se_km = float(np.sqrt(cov[2, 2])) if np.isfinite(cov[2, 2]) else np.nan
        note = ""
    else:
        # Wenn MM nicht plausibel ist: MM-Werte als NaN + kurzen Hinweis
        vmax_h = km_val = se_vmax = se_km = rmse_mm = float("nan")
        note = f"MM verworfen: {reason}"

    return {
        "Probe": label,
        "m": m_val, "m_se": m_se, "RMSE_0": rmse0,
        "k": k1_val, "k_se": k1_se, "RMSE_1": rmse1,
        "r_zehr^max": vmax_h, "r_zehr^max_se": se_vmax,
        "K_M": km_val, "K_M_se": se_km, "RMSE_MM": rmse_mm,
        "MM_Hinweis": note,
    }

#Daten einlesen
def main() -> None:
    """
    Einlesen der Datenblätter, Erzeugen der Plots:
    - Einzelplots mit Fits (Schlick, Steine, Pflanzen 1–3, evtl. extra Blatt)
    - Blank-Sammelplot
    """
    s1 = pd.read_excel("labor_zehrung_steine_schlick.xlsx",
                       sheet_name="Schlick Probe und Blank ", header=None)
    s2 = pd.read_excel("labor_zehrung_steine_schlick.xlsx",
                       sheet_name="Steine Probe  und Blank ", header=None)
    pf = pd.read_excel("zehrung_pflanzen_labor.xlsx",
                       sheet_name="Tabelle1", header=None)

    # Spalten-Zuordnung (manuell/konstant, basierend auf den Dateien)
    t_s, c_s = clean_numeric_cols(s1, 0, 1);   t_sb, c_sb = clean_numeric_cols(s1, 0, 2)
    t_st, c_st = clean_numeric_cols(s2, 0, 1); t_stb, c_stb = clean_numeric_cols(s2, 0, 2)
    t_p1, c_p1 = clean_numeric_cols(pf, 1, 2)
    t_p2, c_p2 = clean_numeric_cols(pf, 3, 4)
    t_p3, c_p3 = clean_numeric_cols(pf, 5, 6)
    t_pb, c_pb = clean_numeric_cols(pf, 9, 8)

    # Probenplots
    plot_with_fits("Schlick Zehrung - Labor", t_s, c_s)
    plot_with_fits("Kiesel Zehrung - Labor", t_st, c_st)
    plot_with_fits("Pflanzenprobe 1 Zehrung - Labor", t_p1, c_p1)
    plot_with_fits("Pflanzenprobe 2 Zehrung - Labor", t_p2, c_p2)
    plot_with_fits("Pflanzenprobe 3 Zehrung - Labor", t_p3, c_p3)

    # Falls in der Pflanzen-Excel noch ein neues Blatt hängt → plotten
    extra_plants = read_last_sheet_pair("zehrung_pflanzen_labor.xlsx", known_primary_sheet="Tabelle1")
    if extra_plants is not None:
        last_name, t_new, c_new = extra_plants
        plot_with_fits(f"{last_name.strip()} Zehrung - Labor", t_new, c_new)

    # Falls in Schlick/Steine-Excel ein zusätzliches Blatt existiert → Pflanzenprobe 4
    extra_schlick = read_last_sheet_pair_excluding(
        "labor_zehrung_steine_schlick.xlsx",
        exclude_names=["Schlick Probe und Blank ", "Steine Probe  und Blank "]
    )
    if extra_schlick is not None:
        _, t4, c4 = extra_schlick
        plot_with_fits("Zehrung - Pflanzenprobe 4", t4, c4)

    # Blanks in einem Plot
    plot_blanks(t_sb, c_sb, t_stb, c_stb, t_pb, c_pb)

def run_parameter_table() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Berechnet alle Kennzahlen, schreibt CSV/LaTeX und gibt (raw, pretty)-DataFrames zurück.
    - „pretty“ formatiert m ± SE usw. direkt für den Bericht
    """
    s1 = pd.read_excel("labor_zehrung_steine_schlick.xlsx",
                       sheet_name="Schlick Probe und Blank ", header=None)
    s2 = pd.read_excel("labor_zehrung_steine_schlick.xlsx",
                       sheet_name="Steine Probe  und Blank ", header=None)
    pf = pd.read_excel("zehrung_pflanzen_labor.xlsx",
                       sheet_name="Tabelle1", header=None)

    # feste Spalten-Indizes gemäß deiner Dateien
    t_s, c_s = clean_numeric_cols(s1, 0, 1)
    t_st, c_st = clean_numeric_cols(s2, 0, 1)
    t_p1, c_p1 = clean_numeric_cols(pf, 1, 2)
    t_p2, c_p2 = clean_numeric_cols(pf, 3, 4)
    t_p3, c_p3 = clean_numeric_cols(pf, 5, 6)

    # Reihenfolge in der Ausgabetabelle
    rows = [
        compute_parameters_for_series("Schlick", t_s, c_s),
        compute_parameters_for_series("Steine", t_st, c_st),
        compute_parameters_for_series("Makro 1", t_p1, c_p1),
        compute_parameters_for_series("Makro 2", t_p2, c_p2),
        compute_parameters_for_series("Makro 3", t_p3, c_p3),
    ]

    # optional: zusätzliches Pflanzen-Blatt am Ende
    extra_plants = read_last_sheet_pair("zehrung_pflanzen_labor.xlsx", known_primary_sheet="Tabelle1")
    if extra_plants is not None:
        last_name, t_new, c_new = extra_plants
        rows.append(compute_parameters_for_series(last_name.strip(), t_new, c_new))

    # optional: zusätzliches Blatt in Schlick/Steine-Excel → als „Pflanzenprobe 4“
    extra_schlick = read_last_sheet_pair_excluding(
        "labor_zehrung_steine_schlick.xlsx",
        exclude_names=["Schlick Probe und Blank ", "Steine Probe  und Blank "]
    )
    if extra_schlick is not None:
        _, t4, c4 = extra_schlick
        rows.append(compute_parameters_for_series("Pflanzenprobe 4", t4, c4))

    df = pd.DataFrame(rows, columns=[
        "Probe", "m", "m_se", "RMSE_0", "k", "k_se", "RMSE_1",
        "r_zehr^max", "r_zehr^max_se", "K_M", "K_M_se", "RMSE_MM", "MM_Hinweis"
    ])

    # Format-Helfer: „v ± se“ bzw. „—“ wenn NaN
    def pm(v: float, se: float) -> str:
        return "—" if (np.isnan(v) or np.isnan(se)) else f"{v:.3f} ± {se:.3f}"

    def fmt(x: float) -> str:
        return "—" if pd.isna(x) else f"{x:.3f}"

    pretty = pd.DataFrame({
        "Probe": df["Probe"],
        "Nullte Ordnung (m) [mg L⁻¹ h⁻¹]": [pm(v, se) for v, se in zip(df["m"], df["m_se"])],
        "RMSE (0) [mg L⁻¹]": df["RMSE_0"].map(fmt),
        "Erste Ordnung (k) [h⁻¹]": [pm(v, se) for v, se in zip(df["k"], df["k_se"])],
        "RMSE (1) [mg L⁻¹]": df["RMSE_1"].map(fmt),
        "r_zehr^max [mg L⁻¹ h⁻¹]": [pm(v, se) for v, se in zip(df["r_zehr^max"], df["r_zehr^max_se"])],
        "K_M [mg L⁻¹]": [pm(v, se) for v, se in zip(df["K_M"], df["K_M_se"])],
        "RMSE (MM) [mg L⁻¹]": df["RMSE_MM"].map(fmt),
        "MM-Hinweis": df["MM_Hinweis"].fillna(""),
    })

    # Konsole (optional hilfreich)
    print("\n--- Parameter (roh) ---")
    print(df.to_string(index=False))
    print("\n--- Parameter (berichtstauglich) ---")
    print(pretty.to_string(index=False))

    # Exports
    df.to_csv("labor_parameter.csv", index=False)
    pretty.to_csv("labor_parameter_pretty.csv", index=False)
    with open("labor_parameter_table.tex", "w", encoding="utf-8") as f:
        f.write(pretty.to_latex(index=False, escape=False,
                                column_format="lcccccccccc"))

    print("\nGespeichert: labor_parameter.csv, labor_parameter_pretty.csv")
    print("LaTeX-Tabelle gespeichert: labor_parameter_table.tex")

    return df, pretty

if __name__ == "__main__":
    # Plots (inkl. optionaler Zusatzblätter)
    main()
    # Tabellen/Exports (inkl. optionaler Zusatzblätter)
    run_parameter_table()
