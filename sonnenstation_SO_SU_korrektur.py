# -*- coding: utf-8 -*-
"""
CSV + LOG PIPELINE (Sonne & Felix) – Interpolation + k(t) (aus Ersatzdaten) +
geometrischer Cosinus-Fit + Ersatz-Plot (S1 & S2) — mit verständlicheren Plots

Was passiert:
- CSVs (Sonnenstation/Felix) + LOGs (*.log, *.txt, *mosquitto-sub*ufp*), Zeitzone Europe/Berlin.
- Priorität: bis 13.08.2025 15:22:00 Sonne; ab 13.08.2025 15:22:57 Felix.
- Interpolation:
    * < 2 Minuten: linear zeitbasiert
    * ≥ 2 Minuten: Tageszeit-Schablone aus Referenztagen (Median), ggf. affine Anpassung (a*Template + b)
- Ausreißer: Gradientenlimit, Hampel, 4σ über 10 min
- Cos-Fit je Tag aus geometrischen Sonnenzeiten (NOAA) für Tübingen
- Ersatz (Blend) nur in definierten Tagesfenstern und nur an Tagen mit genügend hoher Cos-Korrelation
- k(t) = -ln(S2/S1)/d mit d = 0.31 m; Nacht (21:00–05:50) = NaN; Tages-Spikes → NaN → pro Tag kubisch interpoliert
- Exporte (nur >= 04.08.2025 00:00 und <= 17.08.2025 23:59):
    1) merged_sensor12_from_2025-08-04.csv
    2) merged_10min_means_from_2025-08-04_every_10min.csv
    3) k_wert_woche
    4) daily_correlation_cosfit_from_2025-08-04.csv   (S1 & S2)
    5) sonnenstation_korrigiert_1min.csv  (S1+S2: Original, Cos, Blend, Quelle)
    6) sonnenstation_korrigiert_10min.csv

Plot-Layout:
- Liniennamen nur „S1“ / „S2“
- Zeitachse: Major-Tick 12:00 (beschriftet), Minor-Tick 00:00 (unbeschriftet)
- Deutliche Legenden/Notizen, Messlücken und Ersatzfenster visuell markiert
"""

from __future__ import annotations
import re, csv
from pathlib import Path
from typing import Tuple, Optional, List, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.dates import DateFormatter, HourLocator
from matplotlib.lines import Line2D
from zoneinfo import ZoneInfo

# ====================== KONFIG ======================
INPUT_DIR = Path(r"C:\Leon Dietrich\UNI\Feldpraktikum daten\Sonnebearbeitet")
TZ = ZoneInfo("Europe/Berlin")

START_AT  = pd.Timestamp(2025, 8, 4, 0, 0, tz=TZ)
END_AT    = pd.Timestamp(2025, 8, 17, 23, 59, tz=TZ)

# Quelle bevorzugen: bis ... Sonne, ab ... Felix
SWITCH_TIME_SONNE_END   = pd.Timestamp(2025, 8, 13, 15, 22, 0, tz=TZ)
SWITCH_TIME_FELIX_START = pd.Timestamp(2025, 8, 13, 15, 22, 57, tz=TZ)

# --- Optional: simples Zoomfenster für alle Plots ---
# Beide auf None lassen => kein Zoom
X_START = "2025-08-3 23:00"  # z.B. "2025-08-06 00:00"
X_END   = "2025-08-18 01:00"


# Referenztage für Template (für ≥2-min Lücken)
TEMPLATE_PERIODS = [
    (pd.Timestamp(2025, 8, 10, 0, 0, tz=TZ), pd.Timestamp(2025, 8, 11, 0, 0, tz=TZ)),
    (pd.Timestamp(2025, 8, 13, 0, 0, tz=TZ), pd.Timestamp(2025, 8, 14, 0, 0, tz=TZ)),
]

TOLERANCE_SECONDS   = 10
GAP_MINUTES         = 5
PLOT_SMOOTH_MINUTES = 10

GRID_FREQ           = "1T"      # 1-Minuten Raster
SMALL_GAP_LIMIT_MIN = 2         # <2 min → lineare Interpolation
LIMIT_SMALL         = 1         # am Stück erlaubte Lücken für "linear"

LOWER_WM2, UPPER_WM2 = 0.0, 1200.0

# Ausreißer-Filter
DESPIKE_WINDOW = "10T"
DESPIKE_SIGMA  = 4.0
GRAD_MAX_WPM   = 350.0  # max. Sprung pro Minute

# Affiner Fit nur wenn Template über der Lücke genug Variation zeigt
AFFINE_MIN_DENOM = 80.0

# Felix-Kalibrierung
FELIX_S1_FACTOR = 2.0325203252
FELIX_S2_FACTOR = 2.01207243461

# Abstand für k
D_DISTANCE_M = 0.31

# Nachtfenster für k
NIGHT_START_HM = (21, 0)   # 21:00
NIGHT_END_HM   = (6, 50)   # 05:50

# k-Spike-Bereinigung
K_SPIKE_WINDOW_MIN   = 25   # 25 Minuten zurückschauen
K_SPIKE_DELTA_THRESH = 1.5  # 1/m

# Geometrische Sonnenzeiten (NOAA) für Tübingen
LAT_DEG = 48.5216   # +N
LON_DEG = 9.0576    # +E

# Cosine-Quelle (Fallback: CSV >1 W/m²; danach Daten-Detektion)
COS_FILE_NAME = "strahlung_mehrtaegig.csv"
COS_IDEAL_THRESHOLD = 1.0  # W/m²

# Ersatz-Plot: Tagesfenster (lokal) + Korrelation
REPLACE_WINDOWS = [((2, 30), (11, 30)), ((15, 50), (21, 0))]
CORR_MIN_FOR_REPLACE_S1 = 0.90
CORR_MIN_FOR_REPLACE_S2 = 0.90   # separat einstellbar

# Crossfade-Länge (Ein/Ausblendung je Segment, Minuten)
REPLACE_FADE_MIN = 120

# Sunrise/Sunset Übergänge (Minuten)
SUNRISE_LOCK_MIN        = 90   # ab Sunrise so lange NUR Cosinus
SUNRISE_BLEND_TAIL_MIN  = 20   # danach weicher Übergang zurück zum Tages-Blend

SUNSET_BLEND_TAIL_MIN   = 120  # vor Sunset weicher Übergang hin zu 100% Cosinus
SUNSET_LOCK_MIN         = 30   # ab Sunset so lange NUR Cosinus

# Exporte
OUTPUT_FILENAME_RAW       = "merged_sensor12_from_2025-08-04.csv"
OUTPUT_FILENAME_10MIN     = "merged_10min_means_from_2025-08-04_every_10min.csv"
OUTPUT_FILENAME_K         = "k_wert_woche"
OUTPUT_FILENAME_CORR      = "daily_correlation_cosfit_from_2025-08-04.csv"
OUTPUT_FILENAME_REPLOT    = "sonnenstation_korrigiert_1min.csv"
OUTPUT_DELIMITER = ","
# =====================================================

# ---------- Helfer für Plot-Beschriftung ----------
def _format_time_axis_mesz(ax):
    """Nur 12:00 (MESZ) als beschrifteter Major-Tick, 00:00 als unbeschrifteter Minor-Tick."""
    ax.xaxis.set_major_locator(HourLocator(byhour=[12], tz=TZ))
    ax.xaxis.set_minor_locator(HourLocator(byhour=[0],  tz=TZ))
    ax.xaxis.set_major_formatter(DateFormatter("%d.%m. %H:%M", tz=TZ))
    ax.tick_params(axis="x", which="minor", length=4, labelbottom=False)
    
def _apply_zoom(ax):
    """Setzt ein gemeinsames Zoomfenster für die x-Achse, falls definiert."""
    if X_START is not None and X_END is not None:
        ax.set_xlim(pd.Timestamp(X_START, tz=TZ), pd.Timestamp(X_END, tz=TZ))

def _shade_time_gaps(ax, ts_list, gap_minutes=5, alpha=0.18):
    """Schattiert echte Messlücken > gap_minutes (unabhängig von Interpolation)."""
    for i in range(1, len(ts_list)):
        t0, t1 = ts_list[i-1], ts_list[i]
        if pd.isna(t0) or pd.isna(t1):
            continue
        if (t1 - t0) > pd.Timedelta(minutes=gap_minutes):
            ax.axvspan(t0, t1, alpha=alpha, zorder=0)

def _note(ax, text):
    """Kompakte Erläuterung unten links als Textbox."""
    ax.text(0.01, 0.02, text, transform=ax.transAxes, va="bottom", ha="left",
            fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

# ---------- CSV Helfer ----------
def _sniff_delim_and_decimal(p: Path) -> Tuple[str, str]:
    sample = p.read_text(encoding="utf-8", errors="ignore")[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"])
        sep = dialect.delimiter
    except Exception:
        sep = ","
    comma_dec = len(re.findall(r"\d,\d", sample))
    dot_dec   = len(re.findall(r"\d\.\d", sample))
    decimal = "," if comma_dec > dot_dec else "."
    return sep, decimal

def _to_berlin(ts_series: pd.Series) -> pd.Series:
    ts = pd.to_datetime(ts_series, errors="coerce", utc=False)
    if getattr(ts.dt, "tz", None) is None:
        ts = ts.dt.tz_localize(TZ, nonexistent="shift_forward", ambiguous="NaT")
    else:
        ts = ts.dt.tz_convert(TZ)
    return ts

def _find_timestamp_col(df: pd.DataFrame) -> str:
    cols = [c.strip() for c in df.columns]
    low = {c.lower(): c for c in cols}
    for k in ["zeitstempel","zeit","time","timestamp","datetime","datum","date"]:
        if k in low: return low[k]
    return df.columns[0]

def _norm(s: str) -> str:
    return re.sub(r"\s+","", s.strip().lower())

def _pick_col_from_aliases(df: pd.DataFrame, aliases: List[str]) -> Optional[str]:
    df.columns = df.columns.str.strip()
    normmap = {_norm(c): c for c in df.columns}
    for a in aliases:
        na = _norm(a)
        if na in normmap: return normmap[na]
    return None

def _csv_has_sensor_columns(p: Path) -> bool:
    try:
        sep, dec = _sniff_delim_and_decimal(p)
        head = pd.read_csv(p, sep=sep, decimal=dec, nrows=0, engine="python")
        head.columns = head.columns.str.strip()
    except Exception:
        return False
    s1 = _pick_col_from_aliases(head, ["Strahlungsmittel_S1mittel","Strahlung_S1mittel","Strahlung_S1"])
    s2 = _pick_col_from_aliases(head, ["Strahlungsmittel_S2mittel","Strahlung_S2mittel","Strahlung_S2"])
    return (s1 is not None) and (s2 is not None)

def _read_file_strict(p: Path) -> pd.DataFrame:
    sep, decimal = _sniff_delim_and_decimal(p)
    df = pd.read_csv(p, sep=sep, decimal=decimal, engine="python")
    if df.empty: raise ValueError(f"Datei leer: {p.name}")
    df.columns = df.columns.str.strip()
    ts_col = _find_timestamp_col(df); ts = _to_berlin(df[ts_col])
    s1_col = _pick_col_from_aliases(df, ["Strahlungsmittel_S1mittel","Strahlung_S1mittel","Strahlung_S1"])
    s2_col = _pick_col_from_aliases(df, ["Strahlungsmittel_S2mittel","Strahlung_S2mittel","Strahlung_S2"])
    if s1_col is None or s2_col is None:
        raise ValueError(f"In '{p.name}' fehlen Pflichtspalten. Gefunden: {list(df.columns)}")
    s1 = pd.to_numeric(df[s1_col], errors="coerce")
    s2 = pd.to_numeric(df[s2_col], errors="coerce")
    out = pd.DataFrame({"timestamp": ts, "sensor1": s1, "sensor2": s2})
    out = out.dropna(subset=["timestamp"]).sort_values("timestamp").drop_duplicates(subset=["timestamp"])
    return out[(out["timestamp"] >= START_AT) & (out["timestamp"] <= END_AT)]

def _pick_files(folder: Path) -> Tuple[Path, Path]:
    csvs = sorted(folder.rglob("*.csv"))
    eligible = [p for p in csvs if _csv_has_sensor_columns(p)]
    if len(eligible) < 2:
        raise FileNotFoundError("Weniger als zwei geeignete CSVs im Ordner.")
    felix_candidates = [p for p in eligible if "felix" in p.name.lower()]
    sonne_candidates = [p for p in eligible if ("sonnen" in p.name.lower() or "sonne" in p.name.lower()) and "felix" not in p.name.lower()]
    def latest(lst): return sorted(lst, key=lambda x: x.stat().st_mtime, reverse=True)[0]
    felix = latest(felix_candidates) if felix_candidates else latest(eligible)
    rest  = [p for p in eligible if p != felix]
    sonne = latest(sonne_candidates) if sonne_candidates else latest(rest)
    if sonne == felix:
        eligible_sorted = sorted(eligible, key=lambda x: x.stat().st_mtime, reverse=True)
        sonne, felix = eligible_sorted[0], eligible_sorted[1]
    return sonne, felix

def _apply_felix_calibration(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sensor1"] = df["sensor1"].astype(float) * FELIX_S1_FACTOR
    df["sensor2"] = df["sensor2"].astype(float) * FELIX_S2_FACTOR
    return df

# ---------- LOG ----------
LOG_LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+0000)\s+"
    r"ufp/(?P<station>Sonnenstation|Felix)/Sensor_(?P<sensor>[12])/strahlung\s+"
    r"(?P<val>[-+]?\d+(?:\.\d+)?)\s+W/m2\s*$"
)

def _parse_log_file(p: Path) -> List[Dict]:
    rows = []
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = LOG_LINE_RE.match(line.strip())
            if not m: continue
            ts = pd.to_datetime(m.group("ts"), utc=True).tz_convert(TZ)
            rows.append({"timestamp": ts, "station": m.group("station"),
                         "sensor": int(m.group("sensor")), "value": float(m.group("val"))})
    return rows

def _read_logs(folder: Path) -> pd.DataFrame:
    all_rows: List[Dict] = []
    seen = set()
    for pattern in ("*.log", "*.txt", "*mosquitto-sub*ufp*"):
        for p in folder.rglob(pattern):
            if not p.is_file(): continue
            rp = p.resolve()
            if rp in seen: continue
            seen.add(rp)
            all_rows.extend(_parse_log_file(p))
    if not all_rows: return pd.DataFrame(columns=["timestamp","station","sensor","value"])
    df = pd.DataFrame(all_rows).sort_values("timestamp")
    return df[(df["timestamp"] >= START_AT) & (df["timestamp"] <= END_AT)].copy()

def _pivot_logs(df_logs: pd.DataFrame, station_name: str) -> pd.DataFrame:
    df = df_logs[df_logs["station"] == station_name].copy()
    if df.empty: return pd.DataFrame(columns=["timestamp","sensor1","sensor2"])
    wide = df.pivot_table(index="timestamp", columns="sensor", values="value", aggfunc="mean")
    wide = wide.rename(columns={1:"sensor1",2:"sensor2"}).reset_index().sort_values("timestamp")
    return wide[(wide["timestamp"] >= START_AT) & (wide["timestamp"] <= END_AT)]

# ---------- Interpolation & Filter ----------
def _tod_template_minute(series: pd.Series, periods: List[tuple[pd.Timestamp, pd.Timestamp]]) -> pd.Series:
    base = series.copy(); parts = []
    for (start, end) in periods:
        mask = (base.index >= start) & (base.index < end) & (~base.isna())
        parts.append(base[mask])
    ref = pd.concat(parts) if parts else pd.Series(dtype=float)
    if ref.empty:
        return pd.Series(np.zeros(1440), index=np.arange(1440), dtype=float)
    minute = ref.index.hour*60 + ref.index.minute
    med = pd.DataFrame({"m": minute, "v": ref.values}).groupby("m")["v"].median()
    climo = pd.Series(np.nan, index=np.arange(1440), dtype=float)
    climo.loc[med.index.values] = med.values
    return climo.interpolate(limit_direction="both").bfill().ffill()

def _interpolate_with_template(series: pd.Series, climo_minute: pd.Series) -> tuple[pd.Series, pd.Series]:
    s = series.copy(); flags = pd.Series(False, index=s.index)
    vals = s.values; idx = s.index; isna = pd.isna(vals)
    if not isna.any(): return s.clip(LOWER_WM2, UPPER_WM2), flags

    blocks, start = [], None
    for i, na in enumerate(isna):
        if na and start is None: start = i
        if (not na) and (start is not None): blocks.append((start, i-1)); start = None
    if start is not None: blocks.append((start, len(vals)-1))

    def tmpl_at(i: int) -> float:
        m = idx[i].hour*60 + idx[i].minute
        return float(climo_minute.iloc[m])

    for i0, i1 in blocks:
        prev_idx = i0-1
        while prev_idx >= 0 and pd.isna(vals[prev_idx]): prev_idx -= 1
        next_idx = i1+1
        while next_idx < len(vals) and pd.isna(vals[next_idx]): next_idx += 1

        have_prev = prev_idx >= 0
        have_next = next_idx < len(vals)
        c_prev = tmpl_at(prev_idx) if have_prev else np.nan
        y_prev = vals[prev_idx]   if have_prev else np.nan
        c_next = tmpl_at(next_idx) if have_next else np.nan
        y_next = vals[next_idx]    if have_next else np.nan

        use_affine = (np.isfinite(c_prev) and np.isfinite(c_next) and
                      np.isfinite(y_prev) and np.isfinite(y_next) and
                      abs(c_next - c_prev) >= AFFINE_MIN_DENOM)

        if use_affine:
            a = (y_next - y_prev) / (c_next - c_prev)
            b = y_prev - a*c_prev
            fill_vals = np.array([a*tmpl_at(k) + b for k in range(i0, i1+1)], dtype=float)
        else:
            if np.isfinite(c_prev) and c_prev != 0 and np.isfinite(y_prev):
                scale = y_prev / c_prev
            elif np.isfinite(c_next) and c_next != 0 and np.isfinite(y_next):
                scale = y_next / c_next
            else:
                scale = 1.0
            fill_vals = np.array([scale*tmpl_at(k) for k in range(i0, i1+1)], dtype=float)

        s.iloc[i0:i1+1] = fill_vals
        flags.iloc[i0:i1+1] = True

    return s.clip(LOWER_WM2, UPPER_WM2), flags

def _despike_sigma(s: pd.Series, window: str, sigma: float) -> tuple[pd.Series, pd.Series]:
    rmean = s.rolling(window, center=True, min_periods=3).mean()
    rstd  = s.rolling(window, center=True, min_periods=3).std()
    mask  = (s - rmean).abs() > (sigma * rstd)
    mask  = mask & rstd.notna() & (rstd > 0)
    out = s.copy(); out[mask] = np.nan
    return out, mask.fillna(False)

def _hampel(s: pd.Series, window: str, n_sigmas: float) -> tuple[pd.Series, pd.Series]:
    w = pd.to_timedelta(window)
    k = int(max(3, w / pd.to_timedelta("1T")))
    med = s.rolling(k, center=True, min_periods=3).median()
    mad = (s - med).abs().rolling(k, center=True, min_periods=3).median()
    thresh = 1.4826 * mad * n_sigmas
    mask = (s - med).abs() > thresh
    out = s.copy(); out[mask] = np.nan
    return out, mask.fillna(False)

def _limit_gradient(s: pd.Series, max_wpm: float) -> tuple[pd.Series, pd.Series]:
    diff = s.diff()
    mask = diff.abs() > max_wpm
    out = s.copy(); out[mask] = np.nan
    return out, mask.fillna(False)

def _prefer_series(series_by_src: Dict[str, pd.Series], order: List[str]) -> pd.Series:
    out = pd.Series(np.nan, index=next(iter(series_by_src.values())).index, dtype="float64")
    for src in order:
        if src in series_by_src: out = out.where(~out.isna(), series_by_src[src])
    return out

def _apply_range_filter(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").clip(LOWER_WM2, UPPER_WM2)

# ======== COSINE FIT – Sunrise/Sunset aus CSV (>1 W/m²) =========
def _load_cos_sun_windows(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        return pd.DataFrame(columns=["day","sunrise","sunset"])
    sep, dec = _sniff_delim_and_decimal(csv_path)
    df = pd.read_csv(csv_path, sep=sep, decimal=dec, engine="python")
    df.columns = df.columns.str.strip()
    t_col = _find_timestamp_col(df)
    ts = _to_berlin(df[t_col])

    ideal_col = _pick_col_from_aliases(
        df, ["ideal","ideal_wm2","cos","cosine","cosinus","simulation","simuliert","theory","radiation","strahlung_model"]
    )
    if ideal_col is None:
        for c in df.columns:
            if _norm(c).startswith("ideal") or _norm(c).endswith("ideal"):
                ideal_col = c; break
    if ideal_col is None:
        return pd.DataFrame(columns=["day","sunrise","sunset"])

    val = pd.to_numeric(df[ideal_col], errors="coerce")
    tmp = pd.DataFrame({"ts": ts, "v": val}).dropna(subset=["ts"]).sort_values("ts")
    tmp = tmp[(tmp["ts"]>=START_AT) & (tmp["ts"]<=END_AT)]
    if tmp.empty:
        return pd.DataFrame(columns=["day","sunrise","sunset"])

    rows = []
    for gday, gdf in tmp.groupby(tmp["ts"].dt.date):
        pos = gdf[gdf["v"] > COS_IDEAL_THRESHOLD]
        if pos.empty: continue
        sunrise = pos["ts"].iloc[0]
        sunset  = pos["ts"].iloc[-1]
        if (sunset - sunrise) >= pd.Timedelta(hours=6):
            rows.append({"day": gday, "sunrise": sunrise, "sunset": sunset})
    return pd.DataFrame(rows).sort_values("day").reset_index(drop=True)

def _detect_sun_windows_from_data(s1_series: pd.Series,
                                  thresh_wm2: float = 20.0,
                                  bridge_gap: str = "15min") -> pd.DataFrame:
    s = s1_series.copy().sort_index().rolling("5min", min_periods=1).median()
    s = s[(s.index >= START_AT) & (s.index <= END_AT)]
    rows = []
    for day, g in s.groupby(s.index.tz_convert(TZ).date):
        if g.empty: continue
        mask = g > thresh_wm2
        mask = mask.rolling(bridge_gap, min_periods=1).max().astype(bool)
        if not mask.any(): continue
        try:    sunrise = g.index[mask.values.argmax()]
        except: sunrise = pd.NaT
        try:    sunset  = g.index[::-1][mask.values[::-1].argmax()]
        except: sunset  = pd.NaT
        if pd.isna(sunrise) or pd.isna(sunset) or sunset <= sunrise: continue
        if (sunset - sunrise) < pd.Timedelta(hours=6): continue
        rows.append({"day": day, "sunrise": sunrise, "sunset": sunset})
    return pd.DataFrame(rows).sort_values("day").reset_index(drop=True)

# ---------- Geometrische Sonnenauf/-untergänge (NOAA) ----------
def _compute_sun_windows_geom(start_at: pd.Timestamp,
                              end_at: pd.Timestamp,
                              lat_deg: float, lon_deg: float, tz: ZoneInfo) -> pd.DataFrame:
    """Geometrische Sunrise/Sunset (mit Refraktion 90.833°). Ergebnis in tz (MESZ)."""
    if start_at.tz is None:
        start_at = start_at.tz_localize(tz)
    if end_at.tz is None:
        end_at = end_at.tz_localize(tz)

    days = pd.date_range(start_at.date(), end_at.date(), freq="D", tz=tz).date
    phi = np.radians(lat_deg)
    cos_zenith = np.cos(np.radians(90.833))

    rows = []
    for d in days:
        dt_local = pd.Timestamp(d, tz=tz)
        n = int(dt_local.dayofyear)
        gamma = 2.0 * np.pi / 365.0 * (n - 1)

        E = 229.18 * (0.000075
                      + 0.001868 * np.cos(gamma)
                      - 0.032077 * np.sin(gamma)
                      - 0.014615 * np.cos(2 * gamma)
                      - 0.040849 * np.sin(2 * gamma))

        delta = (0.006918
                 - 0.399912 * np.cos(gamma)
                 + 0.070257 * np.sin(gamma)
                 - 0.006758 * np.cos(2 * gamma)
                 + 0.000907 * np.sin(2 * gamma)
                 - 0.002697 * np.cos(3 * gamma)
                 + 0.00148  * np.sin(3 * gamma))

        cos_om0 = (cos_zenith - np.sin(phi) * np.sin(delta)) / (np.cos(phi) * np.cos(delta))
        cos_om0 = np.clip(cos_om0, -1.0, 1.0)
        omega0_deg = np.degrees(np.arccos(cos_om0))

        solar_noon_utc_min = 720.0 - 4.0 * lon_deg - E
        rise_utc_min = solar_noon_utc_min - 4.0 * omega0_deg
        set_utc_min  = solar_noon_utc_min + 4.0 * omega0_deg

        base_utc = pd.Timestamp(d, tz="UTC")
        rise = (base_utc + pd.Timedelta(minutes=float(rise_utc_min))).tz_convert(tz)
        set_  = (base_utc + pd.Timedelta(minutes=float(set_utc_min))).tz_convert(tz)

        if pd.notna(rise) and pd.notna(set_) and (set_ - rise) >= pd.Timedelta(hours=6):
            rows.append({"day": d, "sunrise": rise, "sunset": set_})

    return pd.DataFrame(rows).sort_values("day").reset_index(drop=True)

# ---------- Cos-Fit ----------
def _build_daily_cosfit(index: pd.DatetimeIndex,
                        sun_df: pd.DataFrame,
                        s_for_fit: pd.Series,
                        *,
                        mid_level_wm2: float = 600.0,
                        mid_halfwidth: float = 0.15,
                        ls_min_base: float = 0.2,
                        amp_floor: float = 300.0) -> tuple[pd.Series, pd.DataFrame]:
    """Erzeugt pro Tag einen Kosinus (sinusförmig), skaliert auf die jeweilige Serie s_for_fit."""
    cosfit = pd.Series(0.0, index=index, dtype=float)
    info_rows = []
    if sun_df.empty: return cosfit, pd.DataFrame(columns=["day","sunrise","sunset","amplitude","corr"])

    for _, row in sun_df.iterrows():
        day, rise, set_ = row["day"], row["sunrise"], row["sunset"]
        if pd.isna(rise) or pd.isna(set_) or rise >= set_: continue
        mask = (index >= rise) & (index <= set_)
        if not mask.any(): continue

        t_rel = (index[mask] - rise) / (set_ - rise)
        base  = np.sin(np.pi * t_rel.values)  # [0..1] Tagesbogen
        y     = s_for_fit.reindex(index)[mask].astype(float).values

        mid = np.abs(t_rel.values - 0.5) <= mid_halfwidth
        sel_mid = (mid) & (base >= 0.8) & np.isfinite(y) & (y >= mid_level_wm2)
        if sel_mid.any():
            A = float(np.median(y[sel_mid] / base[sel_mid]))
        else:
            m = (base >= ls_min_base) & np.isfinite(y)
            denom = np.nansum(base[m] ** 2)
            if denom > 0:
                A = float(np.nansum(base[m] * y[m]) / denom)
            else:
                q95 = np.nanpercentile(y, 95)
                A = float(q95) if np.isfinite(q95) else np.nan

        if not np.isfinite(A) or A <= 0: A = amp_floor
        A = float(np.clip(A, 0.0, UPPER_WM2))

        cos_vals = A * base
        cosfit.loc[mask] = cos_vals

        yy = pd.Series(y, index=index[mask])
        cc = pd.Series(cos_vals, index=index[mask])
        valid = yy.notna() & cc.notna() & (cc > 0)
        corr = float(yy[valid].corr(cc[valid])) if valid.sum() >= 10 else np.nan
        info_rows.append({"day": day, "sunrise": rise, "sunset": set_, "amplitude": A, "corr": corr})

    daily_info = pd.DataFrame(info_rows).sort_values("day").reset_index(drop=True)
    return cosfit, daily_info

# ---------- Helfer: Crossfade-Gewichte aus bool-Maske ----------
def _crossfade_weights(mask: pd.Series, fade_min: int) -> pd.Series:
    w = pd.Series(0.0, index=mask.index, dtype=float)
    vals = mask.values
    n = len(vals); i = 0
    while i < n:
        if vals[i]:
            j = i
            while j+1 < n and vals[j+1]: j += 1
            L = j - i + 1
            N = int(min(fade_min, L // 2))
            arr = np.ones(L, dtype=float)
            if N > 0:
                ramp = 0.5 * (1 - np.cos(np.pi * (np.arange(N)+1)/N))
                arr[:N]  = ramp
                arr[-N:] = ramp[::-1]
            w.iloc[i:j+1] = arr
            i = j + 1
        else:
            i += 1
    return w

def _sunrise_lock_mask(index: pd.DatetimeIndex, sun_df: pd.DataFrame, minutes: int, tz: ZoneInfo) -> pd.Series:
    """True in [sunrise, sunrise+minutes) je Tag; Index ist tz-aware."""
    if sun_df is None or sun_df.empty or minutes <= 0:
        return pd.Series(False, index=index)
    mask = pd.Series(False, index=index)
    for _, row in sun_df.iterrows():
        rise = row.get("sunrise", pd.NaT)
        if pd.isna(rise):
            continue
        start = rise
        end   = rise + pd.Timedelta(minutes=minutes)
        seg = (index >= start) & (index < end)
        if seg.any():
            mask.loc[seg] = True
    return mask

def _apply_sunrise_lock_and_tail(base_w: pd.Series,
                                 index: pd.DatetimeIndex,
                                 sun_df: pd.DataFrame,
                                 *,
                                 lock_min: int,
                                 tail_min: int,
                                 enable_mask: pd.Series | None = None) -> pd.Series:
    """[rise, rise+lock)->1.0, danach 'tail_min' weich zurück auf base_w."""
    w = base_w.copy()
    if sun_df is None or sun_df.empty or lock_min <= 0:
        return w
    if enable_mask is None:
        enable_mask = pd.Series(True, index=index)

    for _, row in sun_df.iterrows():
        rise = row.get("sunrise", pd.NaT)
        if pd.isna(rise):
            continue

        t_lock_end = rise + pd.Timedelta(minutes=lock_min)
        sel_lock = (index >= rise) & (index < t_lock_end) & enable_mask
        if sel_lock.any():
            w.loc[sel_lock] = 1.0

        if tail_min > 0:
            t_tail_end = t_lock_end + pd.Timedelta(minutes=tail_min)
            sel_tail = (index >= t_lock_end) & (index < t_tail_end) & enable_mask
            if sel_tail.any():
                r = ((index[sel_tail] - t_lock_end) / pd.Timedelta(minutes=tail_min)).astype(float)
                ramp = 0.5 * (1 - np.cos(np.pi * r))  # 0->1
                w_target = base_w.loc[sel_tail].values
                w.loc[sel_tail] = (1.0 - ramp) * 1.0 + ramp * w_target
    return w

def _apply_sunset_tail_and_lock(base_w: pd.Series,
                                index: pd.DatetimeIndex,
                                sun_df: pd.DataFrame,
                                *,
                                tail_min: int,
                                lock_min: int,
                                enable_mask: pd.Series | None = None) -> pd.Series:
    """Vor Sunset 'tail_min' weich von base_w -> 1.0, danach [set, set+lock)->1.0."""
    w = base_w.copy()
    if sun_df is None or sun_df.empty:
        return w
    if enable_mask is None:
        enable_mask = pd.Series(True, index=index)

    for _, row in sun_df.iterrows():
        set_ = row.get("sunset", pd.NaT)
        if pd.isna(set_):
            continue

        if tail_min > 0:
            t_tail_start = set_ - pd.Timedelta(minutes=tail_min)
            sel_tail = (index >= t_tail_start) & (index < set_) & enable_mask
            if sel_tail.any():
                r = ((index[sel_tail] - t_tail_start) / pd.Timedelta(minutes=tail_min)).astype(float)
                ramp = 0.5 * (1 - np.cos(np.pi * r))  # 0->1
                w_base = base_w.loc[sel_tail].values
                w.loc[sel_tail] = (1.0 - ramp) * w_base + ramp * 1.0

        if lock_min > 0:
            t_lock_end = set_ + pd.Timedelta(minutes=lock_min)
            sel_lock = (index >= set_) & (index < t_lock_end) & enable_mask
            if sel_lock.any():
                w.loc[sel_lock] = 1.0
    return w

# ====================== MAIN ======================
def main():
    # ---- CSVs lesen ----
    sonne_path, felix_path = _pick_files(INPUT_DIR)
    print(f"CSV gefunden:\n  Sonne: {sonne_path.name}\n  Felix: {felix_path.name}")
    df_sonne = _read_file_strict(sonne_path)
    df_felix = _read_file_strict(felix_path)
    df_felix = _apply_felix_calibration(df_felix)
    if df_sonne.empty and df_felix.empty:
        raise ValueError("Keine CSV-Daten im Zeitraum.")

    # Union-Timeline
    union_ts = pd.Index(sorted(pd.unique(pd.concat([df_sonne["timestamp"], df_felix["timestamp"]]))))
    union_ts = union_ts[(union_ts >= START_AT) & (union_ts <= END_AT)]
    timeline = pd.DataFrame({"timestamp": union_ts})
    tol = pd.Timedelta(seconds=TOLERANCE_SECONDS)

    # As-of Merge CSV
    m_sonne = pd.merge_asof(timeline[["timestamp"]], df_sonne, on="timestamp",
                            direction="nearest", tolerance=tol)
    m_felix = pd.merge_asof(timeline[["timestamp"]], df_felix, on="timestamp",
                            direction="nearest", tolerance=tol)

    # Quellenpräferenz
    csv_s1_before = _prefer_series({"sonne": m_sonne["sensor1"], "felix": m_felix["sensor1"]}, ["sonne","felix"])
    csv_s2_before = _prefer_series({"sonne": m_sonne["sensor2"], "felix": m_felix["sensor2"]}, ["sonne","felix"])
    csv_s1_after  = _prefer_series({"felix": m_felix["sensor1"], "sonne": m_sonne["sensor1"]}, ["felix","sonne"])
    csv_s2_after  = _prefer_series({"felix": m_felix["sensor2"], "sonne": m_sonne["sensor2"]}, ["felix","sonne"])

    merged = timeline.copy()
    mask_before  = merged["timestamp"] <= SWITCH_TIME_SONNE_END
    mask_after   = merged["timestamp"] >= SWITCH_TIME_FELIX_START
    mask_between = (~mask_before) & (~mask_after)
    merged["sensor1"] = np.where(mask_after, csv_s1_after, csv_s1_before)
    merged["sensor2"] = np.where(mask_after, csv_s2_after, csv_s2_before)
    merged.loc[mask_between, ["sensor1","sensor2"]] = np.c_[
        csv_s1_before[mask_between], csv_s2_before[mask_between]
    ]

    # ---- LOGs lesen & als Fallback verwenden ----
    logs_df = _read_logs(INPUT_DIR)
    if not logs_df.empty:
        log_sonne = _pivot_logs(logs_df, "Sonnenstation")
        log_felix = _pivot_logs(logs_df, "Felix")
        if not log_felix.empty: log_felix = _apply_felix_calibration(log_felix)

        def asof_log(src):
            return (pd.merge_asof(timeline[["timestamp"]], src.sort_values("timestamp"),
                                  on="timestamp", direction="nearest", tolerance=tol)
                    if not src.empty else timeline.assign(sensor1=np.nan, sensor2=np.nan))

        mlog_sonne = asof_log(log_sonne).rename(columns={"sensor1":"ls1","sensor2":"ls2"})
        mlog_felix = asof_log(log_felix).rename(columns={"sensor1":"lf1","sensor2":"lf2"})

        for col, sson, sfel in [("sensor1","ls1","lf1"), ("sensor2","ls2","lf2")]:
            na = merged[col].isna()
            fill_before = na & (mask_before | mask_between)
            merged.loc[fill_before, col] = mlog_sonne[sson][fill_before]
            still_na   = merged[col].isna() & (mask_before | mask_between)
            merged.loc[still_na, col] = mlog_felix[sfel][still_na]
            fill_after = merged[col].isna() & mask_after
            merged.loc[fill_after, col] = mlog_felix[sfel][fill_after]
            still_na2  = merged[col].isna() & mask_after
            merged.loc[still_na2, col] = mlog_sonne[sson][still_na2]

    # ---- auf 1-Minuten-Raster ----
    merged = merged.sort_values("timestamp").reset_index(drop=True)
    obs_ts = merged["timestamp"].dropna().sort_values().reset_index(drop=True)
    if len(obs_ts) == 0:
        raise ValueError("Keine Zeitstempel verfügbar.")
    grid_start = max(START_AT, obs_ts.min().floor(GRID_FREQ))
    grid_end   = min(END_AT,   obs_ts.max().ceil(GRID_FREQ))
    grid = pd.date_range(grid_start, grid_end, freq=GRID_FREQ, tz=TZ)

    on_grid = pd.DataFrame(index=grid).join(
        merged.set_index("timestamp")[["sensor1","sensor2"]], how="left"
    )
    on_grid["sensor1"] = _apply_range_filter(on_grid["sensor1"])
    on_grid["sensor2"] = _apply_range_filter(on_grid["sensor2"])

    # <2 min: lineare Zeitinterpolation
    s1_lin = on_grid["sensor1"].interpolate(method="time", limit=LIMIT_SMALL, limit_direction="both")
    s2_lin = on_grid["sensor2"].interpolate(method="time", limit=LIMIT_SMALL, limit_direction="both")
    f1_small = s1_lin.notna() & on_grid["sensor1"].isna()
    f2_small = s2_lin.notna() & on_grid["sensor2"].isna()

    # ≥2 min: Template
    cl1 = _tod_template_minute(on_grid["sensor1"], TEMPLATE_PERIODS)
    cl2 = _tod_template_minute(on_grid["sensor2"], TEMPLATE_PERIODS)
    s1_big, f1_big = _interpolate_with_template(s1_lin, cl1)
    s2_big, f2_big = _interpolate_with_template(s2_lin, cl2)

    filled = pd.DataFrame({"sensor1": s1_big.clip(LOWER_WM2, UPPER_WM2),
                           "sensor2": s2_big.clip(LOWER_WM2, UPPER_WM2)}, index=on_grid.index)
    flags = pd.DataFrame({"Flag_S1": (f1_small|f1_big).astype(bool),
                          "Flag_S2": (f2_small|f2_big).astype(bool)}, index=on_grid.index)

    # Ausreißerfilter
    g1, m1 = _limit_gradient(filled["sensor1"], GRAD_MAX_WPM)
    g2, m2 = _limit_gradient(filled["sensor2"], GRAD_MAX_WPM)
    g1 = g1.interpolate(method="time", limit=LIMIT_SMALL, limit_direction="both")
    g2 = g2.interpolate(method="time", limit=LIMIT_SMALL, limit_direction="both")
    h1, h1m = _hampel(g1, DESPIKE_WINDOW, 4.0);  s1d, s1m = _despike_sigma(h1, DESPIKE_WINDOW, DESPIKE_SIGMA)
    h2, h2m = _hampel(g2, DESPIKE_WINDOW, 4.0);  s2d, s2m = _despike_sigma(h2, DESPIKE_WINDOW, DESPIKE_SIGMA)
    s1_post = s1d.interpolate(method="time", limit=LIMIT_SMALL, limit_direction="both").clip(LOWER_WM2, UPPER_WM2)
    s2_post = s2d.interpolate(method="time", limit=LIMIT_SMALL, limit_direction="both").clip(LOWER_WM2, UPPER_WM2)
    filled["sensor1"] = s1_post; filled["sensor2"] = s2_post
    flags["Flag_S1"] |= (m1 | h1m | s1m)
    flags["Flag_S2"] |= (m2 | h2m | s2m)

    # ===================== COSINE FIT =====================
    # 1) Geometrische Zeiten (NOAA) für Tübingen
    sun_df = _compute_sun_windows_geom(START_AT, END_AT, LAT_DEG, LON_DEG, TZ)

    # 2) Fallback: CSV (falls vorhanden)
    if sun_df.empty:
        cos_csv = INPUT_DIR / COS_FILE_NAME
        sun_df  = _load_cos_sun_windows(cos_csv)

    # 3) Fallback: aus Daten detektieren
    if sun_df.empty:
        print("Hinweis: keine geometrischen/CSV-Fenster – detektiere aus Sensor1 …")
        sun_df = _detect_sun_windows_from_data(filled["sensor1"])
        if sun_df.empty:
            print("Warnung: Auch Daten-Detektion ergab keine Tagesfenster – Kosinus-Fit wird ausgelassen.")

    # Cos-Fits getrennt für S1 und S2
    s1_for_fit = filled["sensor1"].copy()
    s2_for_fit = filled["sensor2"].copy()

    cosfit1 = pd.Series(0.0, index=filled.index)
    cosfit2 = pd.Series(0.0, index=filled.index)
    daily_info1 = pd.DataFrame(columns=["day","sunrise","sunset","amplitude","corr"])
    daily_info2 = pd.DataFrame(columns=["day","sunrise","sunset","amplitude","corr"])

    if not sun_df.empty:
        cosfit1, daily_info1 = _build_daily_cosfit(filled.index, sun_df, s1_for_fit)
        cosfit2, daily_info2 = _build_daily_cosfit(filled.index, sun_df, s2_for_fit)

        # Mergen der Tagesinfos (S1 & S2) für Export/Print
        di = daily_info1.rename(columns={"amplitude":"amplitude_s1","corr":"corr_s1"})
        dj = daily_info2.rename(columns={"amplitude":"amplitude_s2","corr":"corr_s2"})
        daily_info = pd.merge(di, dj[["day","amplitude_s2","corr_s2"]], on="day", how="outer")
        daily_info = daily_info.sort_values("day").reset_index(drop=True)
        daily_info["used_for_replacement_s1"] = daily_info["corr_s1"] > CORR_MIN_FOR_REPLACE_S1
        daily_info["used_for_replacement_s2"] = daily_info["corr_s2"] > CORR_MIN_FOR_REPLACE_S2

        # Export + PRINT der Korrelationen
        out_corr = INPUT_DIR / OUTPUT_FILENAME_CORR
        daily_info.to_csv(out_corr, index=False, sep=OUTPUT_DELIMITER)
        print("\n=== Tägliche Korrelationen Cosinus-Fit (MESZ-Tage) ===")
        if not daily_info.empty:
            dfp = daily_info.copy()
            dfp["day"] = dfp["day"].astype(str)
            for col in ["sunrise","sunset"]:
                if col in dfp:
                    dfp[col] = dfp[col].dt.tz_convert(TZ).dt.strftime("%Y-%m-%d %H:%M")
            cols = ["day","sunrise","sunset","amplitude_s1","corr_s1","used_for_replacement_s1",
                    "amplitude_s2","corr_s2","used_for_replacement_s2"]
            print(dfp[cols].to_string(index=False))
        print(f"(Exportiert nach: {out_corr.resolve()})\n")

    # ===================== Exporte Sensoren (Original-gefüllt) =====================
    obs_ts_clip = obs_ts[(obs_ts >= START_AT) & (obs_ts <= END_AT)]

    gap_starts = []
    for i in range(1, len(obs_ts_clip)):
        if (obs_ts_clip[i] - obs_ts_clip[i-1]) > pd.Timedelta(minutes=GAP_MINUTES):
            gap_starts.append(obs_ts_clip[i])

    export_df = filled.copy().reset_index().rename(columns={"index":"timestamp"})
    for t in gap_starts:
        t_mark = t.ceil(GRID_FREQ)
        if START_AT <= t_mark <= END_AT:
            export_df.loc[export_df["timestamp"] == t_mark, "timestamp"] = pd.NaT

    flags.index.name = "timestamp"
    export_df = export_df.merge(flags.reset_index(), on="timestamp", how="left")
    export_df[["Flag_S1","Flag_S2"]] = export_df[["Flag_S1","Flag_S2"]].fillna(False)
    export_df["Flag_S1"] = np.where(export_df["Flag_S1"], "interpol", "")
    export_df["Flag_S2"] = np.where(export_df["Flag_S2"], "interpol", "")
    export_df = export_df[(export_df["timestamp"].isna()) |
                          ((export_df["timestamp"] >= START_AT) & (export_df["timestamp"] <= END_AT))]
    out1 = INPUT_DIR / OUTPUT_FILENAME_RAW
    export_df.rename(columns={"sensor1":"Strahlungsmittel_S1mittel",
                              "sensor2":"Strahlungsmittel_S2mittel"}).to_csv(out1, index=False, sep=OUTPUT_DELIMITER)
    print(f"Export (roh) geschrieben: {out1.resolve()}")

    # 10-min-Mittel (unglättet)
    ts_df = filled[(~filled.index.isna()) & (filled.index >= START_AT) & (filled.index <= END_AT)]
    try:
        resampled = ts_df.resample("10T", origin=START_AT, label="left", closed="left").mean(numeric_only=True)
    except TypeError:
        resampled = ts_df.resample("10T", origin=START_AT, label="left", closed="left").mean()
    flag10 = flags[(~flags.index.isna()) & (flags.index >= START_AT) & (flags.index <= END_AT)].resample(
        "10T", origin=START_AT, label="left", closed="left").max().astype(bool)
    fixed_index = pd.date_range(start=START_AT, end=END_AT, freq="10T", tz=TZ)
    resampled = resampled.reindex(fixed_index); flag10 = flag10.reindex(fixed_index).fillna(False)
    export_10min = resampled.rename(columns={"sensor1":"Strahlungsmittel_S1mittel",
                                             "sensor2":"Strahlungsmittel_S2mittel"}).reset_index()
    export_10min = export_10min.rename(columns={"index":"timestamp"})
    export_10min["Flag_S1"] = np.where(flag10["Flag_S1"].values, "interpol", "")
    export_10min["Flag_S2"] = np.where(flag10["Flag_S2"].values, "interpol", "")
    out2 = INPUT_DIR / OUTPUT_FILENAME_10MIN
    export_10min.to_csv(out2, index=False, sep=OUTPUT_DELIMITER)
    print(f"Export (10-min-Mittel) geschrieben: {out2.resolve()}")

    # ===================== Cos-Ersatzmaske & Crossfade (S1 & S2) =====================
    if 'daily_info' in locals() and not daily_info.empty:
        high_days_s1 = set(d for d, r in zip(daily_info["day"], daily_info["corr_s1"]) if (pd.notna(r) and r > CORR_MIN_FOR_REPLACE_S1))
        high_days_s2 = set(d for d, r in zip(daily_info["day"], daily_info["corr_s2"]) if (pd.notna(r) and r > CORR_MIN_FOR_REPLACE_S2))
    else:
        high_days_s1, high_days_s2 = set(), set()

    idx_local_fill = filled.index.tz_convert(TZ)
    tmin_all = idx_local_fill.hour*60 + idx_local_fill.minute

    def _winmask_tod(tmin_all: np.ndarray, h1m, h2m):
        h1, m1 = h1m; h2, m2 = h2m
        return (tmin_all >= h1*60+m1) & (tmin_all < h2*60+m2)

    win_mask = pd.Series(False, index=filled.index)
    for (s_hm, e_hm) in REPLACE_WINDOWS:
        win_mask |= pd.Series(_winmask_tod(tmin_all, s_hm, e_hm), index=filled.index)

    day_dates = pd.Index(idx_local_fill.date, dtype="object")
    mask_day_high_s1 = pd.Series([d in high_days_s1 for d in day_dates], index=filled.index) if len(high_days_s1)>0 else pd.Series(False, index=filled.index)
    mask_day_high_s2 = pd.Series([d in high_days_s2 for d in day_dates], index=filled.index) if len(high_days_s2)>0 else pd.Series(False, index=filled.index)

    cosfit_series1 = pd.Series(cosfit1, index=filled.index) if 'cosfit1' in locals() else pd.Series(0.0, index=filled.index)
    cosfit_series2 = pd.Series(cosfit2, index=filled.index) if 'cosfit2' in locals() else pd.Series(0.0, index=filled.index)

    replace_mask1 = (cosfit_series1 > 0.0) & win_mask & mask_day_high_s1
    replace_mask2 = (cosfit_series2 > 0.0) & win_mask & mask_day_high_s2

    # Crossfade-Gewichte aus Tagesfenstern
    w1 = _crossfade_weights(replace_mask1, REPLACE_FADE_MIN)
    w2 = _crossfade_weights(replace_mask2, REPLACE_FADE_MIN)

    # optional: nur auf „gute Tage“ begrenzen
    enable1 = (mask_day_high_s1 & (cosfit_series1 > 0)).reindex(filled.index, fill_value=False)
    enable2 = (mask_day_high_s2 & (cosfit_series2 > 0)).reindex(filled.index, fill_value=False)

    # Sonnenaufgang/untergang Übergänge
    w1 = _apply_sunrise_lock_and_tail(w1, filled.index, sun_df,
                                      lock_min=SUNRISE_LOCK_MIN,
                                      tail_min=SUNRISE_BLEND_TAIL_MIN,
                                      enable_mask=enable1)
    w2 = _apply_sunrise_lock_and_tail(w2, filled.index, sun_df,
                                      lock_min=SUNRISE_LOCK_MIN,
                                      tail_min=SUNRISE_BLEND_TAIL_MIN,
                                      enable_mask=enable2)

    w1 = _apply_sunset_tail_and_lock(w1, filled.index, sun_df,
                                     tail_min=SUNSET_BLEND_TAIL_MIN,
                                     lock_min=SUNSET_LOCK_MIN,
                                     enable_mask=enable1)
    w2 = _apply_sunset_tail_and_lock(w2, filled.index, sun_df,
                                     tail_min=SUNSET_BLEND_TAIL_MIN,
                                     lock_min=SUNSET_LOCK_MIN,
                                     enable_mask=enable2)

    # --- Sonnenaufgang: ausschließlich Cosinus (kein Blending) ---
    lock_mask = _sunrise_lock_mask(filled.index, sun_df, SUNRISE_LOCK_MIN, TZ)
    lock1 = lock_mask & mask_day_high_s1 & (cosfit_series1 > 0)
    lock2 = lock_mask & mask_day_high_s2 & (cosfit_series2 > 0)
    w1.loc[lock1] = 1.0
    w2.loc[lock2] = 1.0

    # Blend S1 / S2
    s1_orig = filled["sensor1"].astype(float)
    s2_orig = filled["sensor2"].astype(float)
    s1_blend = (1.0 - w1) * s1_orig + w1 * cosfit_series1
    s2_blend = (1.0 - w2) * s2_orig + w2 * cosfit_series2

    # Export der Plotserie (Ersatzdaten, S1 & S2)
    source1 = np.where(w1.values == 0.0, "original",
                       np.where(w1.values == 1.0, "cosine", "blend"))
    source2 = np.where(w2.values == 0.0, "original",
                       np.where(w2.values == 1.0, "cosine", "blend"))
    export_plot = pd.DataFrame({
        "timestamp": filled.index,
        # S1
        "S1_original": s1_orig.values,
        "S1_cosfit": cosfit_series1.values,
        "S1_plot_blended": s1_blend.values,
        "blend_weight_s1": w1.values,
        "source_s1": source1,
        # S2
        "S2_original": s2_orig.values,
        "S2_cosfit": cosfit_series2.values,
        "S2_plot_blended": s2_blend.values,
        "blend_weight_s2": w2.values,
        "source_s2": source2,
    })
    export_plot = export_plot[(export_plot["timestamp"] >= START_AT) & (export_plot["timestamp"] <= END_AT)]
    outp = INPUT_DIR / OUTPUT_FILENAME_REPLOT
    export_plot.to_csv(outp, index=False, sep=OUTPUT_DELIMITER)
    print(f"Ersatz-Plot-Serie (S1&S2) exportiert: {outp.resolve()}")

    # ===== 10-min-Mittel der ERSATZDATEN (Blend) ab 04.08.2025 00:00 =====
    OUTPUT_FILENAME_REPLOT_10MIN = "sonnenstation_korrigiert_10min.csv"
    blend_series = pd.DataFrame({
        "S1_plot_blended": s1_blend,
        "S2_plot_blended": s2_blend
        }, index=filled.index)
    blend_series = blend_series[(blend_series.index >= START_AT) & (blend_series.index <= END_AT)]
    try:
        repl_10 = blend_series.resample("10T", origin=START_AT, label="left", closed="left") \
                              .mean(numeric_only=True)
    except TypeError:
        repl_10 = blend_series.resample("10T", origin=START_AT, label="left", closed="left").mean()
    fixed_10_idx = pd.date_range(start=START_AT, end=END_AT, freq="10T", tz=TZ)
    repl_10 = repl_10.reindex(fixed_10_idx)
    repl_10 = repl_10.reset_index().rename(columns={"index": "timestamp"})
    outp10 = INPUT_DIR / OUTPUT_FILENAME_REPLOT_10MIN
    repl_10.to_csv(outp10, index=False, sep=OUTPUT_DELIMITER)
    print(f"Ersatz-Plot-Serie (10-min-Mittel) exportiert: {outp10.resolve()}")

    # ===================== k(t) — jetzt aus ERSATZDATEN =====================
    # WICHTIG: k wird aus den Blend-Serien berechnet (wie gewünscht)
    s1_k = s1_blend
    s2_k = s2_blend
    valid = (s1_k > 0) & (s2_k > 0) & (s2_k <= s1_k)
    k = pd.Series(np.nan, index=filled.index, dtype=float)
    k.loc[valid] = -np.log((s2_k.loc[valid] / s1_k.loc[valid]).astype(float)) / D_DISTANCE_M  # 1/m

    # Nacht = NaN
    idx_local = k.index.tz_convert(TZ)
    tod_min = pd.Series(idx_local.hour*60 + idx_local.minute + idx_local.second/60.0, index=k.index)
    start_min = NIGHT_START_HM[0]*60 + NIGHT_START_HM[1]
    end_min   = NIGHT_END_HM[0]*60 + NIGHT_END_HM[1]
    if start_min <= end_min:
        night_mask = (tod_min >= start_min) & (tod_min < end_min)
    else:
        night_mask = (tod_min >= start_min) | (tod_min < end_min)
    night_mask = night_mask.astype(bool)
    k.loc[night_mask] = np.nan

    # Spike-Fenster → NaN → pro Tag kubisch füllen (Nacht bleibt NaN)
    k_shift = k.shift(K_SPIKE_WINDOW_MIN)
    core = k.notna() & k_shift.notna() & ((k - k_shift).abs() > K_SPIKE_DELTA_THRESH)
    window_mask = core[::-1].rolling(K_SPIKE_WINDOW_MIN, min_periods=1).max().astype(bool)[::-1]

    def _interp_day_cubic(series: pd.Series, night_mask: pd.Series) -> pd.Series:
        out = []
        for _, s_day in series.groupby(series.index.tz_convert(TZ).date):
            try:
                s_i = s_day.interpolate(method="spline", order=3, limit_direction="both")
            except Exception:
                s_i = s_day.interpolate(method="polynomial", order=3, limit_direction="both")
            nm = night_mask.loc[s_i.index]
            s_i.loc[nm] = np.nan
            out.append(s_i)
        return pd.concat(out).sort_index()

    k_clean = k.copy()
    mask_to_interp = (~night_mask) & window_mask
    k_clean[mask_to_interp] = np.nan
    k_clean = _interp_day_cubic(k_clean, night_mask)

    # Export k(t) – Flag markiert Interpolation ODER Blend-Verwendung
    # (Blend genutzt, wenn w1>0 oder w2>0)
    blend_used = ((w1 > 0) | (w2 > 0)).reindex(k_clean.index).fillna(False)

    k_export = pd.DataFrame({
        "timestamp": k_clean.index,
        "k_sonne_1_per_m": k_clean.values,
        "Flag_k": np.where((
            ((flags["Flag_S1"]|flags["Flag_S2"]).reindex(k_clean.index).fillna(False))
            | window_mask.reindex(k_clean.index).fillna(False)
            | blend_used.values
        ), "interpol", "")
    })
    k_export = k_export[(k_export["timestamp"] >= START_AT) & (k_export["timestamp"] <= END_AT)]
    outk = INPUT_DIR / OUTPUT_FILENAME_K
    k_export.to_csv(outk, index=False, sep=OUTPUT_DELIMITER)
    print(f"Export k(t) geschrieben: {outk.resolve()}")

    # ===================== PLOTS (MESZ) =====================
    # 1) Strahlung (geglättet) + Cosinus-Fits + Messlücken
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    _shade_time_gaps(ax, obs_ts_clip, gap_minutes=GAP_MINUTES, alpha=0.18)

    smooth = filled.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
    smooth = smooth[(smooth.index >= START_AT) & (smooth.index <= END_AT)]
    ax.plot(smooth.index, smooth["sensor1"], label="SO")
    ax.plot(smooth.index, smooth["sensor2"], label="SU")

    if 'cosfit1' in locals() and not sun_df.empty:
        cos1 = pd.Series(cosfit1, index=filled.index).rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
        cos1 = cos1[(cos1.index >= START_AT) & (cos1.index <= END_AT)]
        ax.plot(cos1.index, cos1.values, linestyle="--", linewidth=2.0, alpha=0.9, color="k",
                label="Kosinus-Fit S1")

    if 'cosfit2' in locals() and not sun_df.empty:
        cos2 = pd.Series(cosfit2, index=filled.index).rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
        cos2 = cos2[(cos2.index >= START_AT) & (cos2.index <= END_AT)]
        ax.plot(cos2.index, cos2.values, linestyle=":", linewidth=2.0, alpha=0.9, color="k",
                label="Kosinus-Fit S2")

    ax.set_xlabel("Zeit (MESZ)")
    ax.set_ylabel("Strahlung [W/m²]")
    #ax.set_title("Strahlung SO & SU – 10-min geglättet, geometrischer Cosinus-Tagesbogen und Messlücken")
    ax.set_ylim(bottom=0, top=1300)
    _format_time_axis_mesz(ax)  
    _apply_zoom(ax)
    ax.grid(True, which="major", alpha=0.45)
    ax.grid(True, which="minor", alpha=0.25)
    plt.setp(ax.get_xticklabels(), rotation=55, ha="right")

    gap_patch = Patch(alpha=0.18, label=f"Messlücke > {GAP_MINUTES} min")
    ax.legend(handles=ax.get_lines() + [gap_patch], loc="best")

    #_note(ax, "Linien: 10-min-Mittel (geglättet). Cosinus-Fit basiert auf geometrischen Sonnenzeiten.\n"
    #          "Schattierung: Zeitabschnitte ohne Messpunkte (>5 min Lücke).")
    plt.tight_layout(); plt.show()

    # 2) k(t) – aus Blend-Daten, Nacht entfernt
    k_smooth = k_clean.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
    k_smooth = k_smooth[(k_smooth.index >= START_AT) & (k_smooth.index <= END_AT)]

    fig2, ax2 = plt.subplots(figsize=(12.5, 5.6))
    ax2.plot(k_smooth.index, k_smooth.values, label="k(t) – 10-min geglättet")
    ax2.set_xlabel("Zeit (MESZ)")
    ax2.set_ylabel("Extinktionskoeffizient k [1/m]")
    #ax2.set_title("Extinktionskoeffizient k(t) aus SO/SU (ersetzte/gebänderte Reihen) – Nacht entfernt")

    _format_time_axis_mesz(ax2)
    _apply_zoom(ax2)
    ax2.grid(True, which="major", alpha=0.45)
    ax2.grid(True, which="minor", alpha=0.25)
    plt.setp(ax2.get_xticklabels(), rotation=55, ha="right")
    ax2.legend(loc="best")

    #_note(ax2, "Berechnung: k = −ln(S2/S1)/d mit d = 0.31 m. Nacht (21:00–05:50) = NaN.\n"
     #          "Spikes → NaN → pro Tag kubisch interpoliert (nur außerhalb der Nacht).\n"
      #         "k basiert hier auf den ersetzten/gebänderten Reihen (Cos-Blend).")
    plt.tight_layout(); plt.show()

    # 3) Sensor 1 – Original vs. Ersatz + markierte Ersatzfenster
    s1_blend_smooth = s1_blend.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
    s1_orig_smooth  = s1_orig.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
    s1_blend_smooth = s1_blend_smooth[(s1_blend_smooth.index >= START_AT) & (s1_blend_smooth.index <= END_AT)]
    s1_orig_smooth  = s1_orig_smooth[(s1_orig_smooth.index >= START_AT) & (s1_orig_smooth.index <= END_AT)]

    fig3, ax3 = plt.subplots(figsize=(12.5, 6.2))
    w1_clip = w1[(w1.index >= START_AT) & (w1.index <= END_AT)]
    w1_vals = w1_clip.values; idx_w1 = w1_clip.index
    i = 0
    while i < len(w1_vals):
        if w1_vals[i] > 0:
            j = i
            while j + 1 < len(w1_vals) and w1_vals[j + 1] > 0:
                j += 1
            ax3.axvspan(idx_w1[i], idx_w1[j], alpha=0.18, zorder=0)
            i = j + 1
        else:
            i += 1

    line_meas, = ax3.plot(s1_orig_smooth.index,  s1_orig_smooth.values) #,  label="S1")
    ax3.plot(s1_blend_smooth.index, s1_blend_smooth.values, linestyle="--", alpha=0.9, label="_nolegend_")

    ax3.set_xlabel("Zeit (MESZ)")
    ax3.set_ylabel("Strahlung [W/m²]")
    #ax3.set_title("Sensor SO: gemessen vs. Ersatz (Cos-Blend) – Ersatzfenster hervorgehoben")
    ax3.set_ylim(bottom=0, top=UPPER_WM2)

    _format_time_axis_mesz(ax3)
    _apply_zoom(ax3)
    ax3.grid(True, which="major", alpha=0.45)
    ax3.grid(True, which="minor", alpha=0.25)
    plt.setp(ax3.get_xticklabels(), rotation=55, ha="right")

    style_meas  = Line2D([0],[0], linestyle="-",  label="gemessen (geglättet)")
    style_blend = Line2D([0],[0], linestyle="--", color="orange", label="Ersatz/Blend (Cos-Fit)")
    patch_w1    = Patch(alpha=0.18, label="Zeitfenster mit Ersatz (SO)")
    ax3.legend(handles=[line_meas, style_meas, style_blend, patch_w1], loc="best")

    #_note(ax3, "Ersatzdaten entstehen durch Crossfade zum Cosinus-Fit,\n"
     #          "nur in markierten Tagesfenstern und nur an Tagen mit guter Übereinstimmung.")
    plt.tight_layout(); plt.show()

    # 4) Nur ERSATZ (S1)
    fig4, ax4 = plt.subplots(figsize=(12.5, 6.0))
    ax4.plot(s1_blend_smooth.index, s1_blend_smooth.values, label="SO neu")
    ax4.set_xlabel("Zeit (MESZ)")
    ax4.set_ylabel("Strahlung [W/m²]")
    #ax4.set_title("Sensor SO – Blend (10-min geglättet)")
    ax4.set_ylim(bottom=0, top=UPPER_WM2)

    _format_time_axis_mesz(ax4)
    _apply_zoom(ax4)
    ax4.grid(True, which="major", alpha=0.45)
    ax4.grid(True, which="minor", alpha=0.25)
    plt.setp(ax4.get_xticklabels(), rotation=55, ha="right")
    ax4.legend(loc="best")
    #_note(ax4, "Gezeigt wird ausschließlich die ersetzte/gebänderte Serie von S1.")
    plt.tight_layout(); plt.show()

    # 5) Sensor 2 – Original vs. Ersatz + markierte Ersatzfenster
    s2_blend_smooth = s2_blend.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
    s2_orig_smooth  = s2_orig.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()
    s2_blend_smooth = s2_blend_smooth[(s2_blend_smooth.index >= START_AT) & (s2_blend_smooth.index <= END_AT)]
    s2_orig_smooth  = s2_orig_smooth[(s2_orig_smooth.index >= START_AT) & (s2_orig_smooth.index <= END_AT)]

    fig5, ax5 = plt.subplots(figsize=(12.5, 6.2))
    w2_clip = w2[(w2.index >= START_AT) & (w2.index <= END_AT)]
    w2_vals = w2_clip.values; idx_w2 = w2_clip.index
    i = 0
    while i < len(w2_vals):
        if w2_vals[i] > 0:
            j = i
            while j + 1 < len(w2_vals) and w2_vals[j + 1] > 0:
                j += 1
            ax5.axvspan(idx_w2[i], idx_w2[j], alpha=0.18, zorder=0)
            i = j + 1
        else:
            i += 1

    line_meas2, = ax5.plot(s1_blend_smooth.index, s1_blend_smooth.values, label="SO neu")
    
    ax5.plot(s2_blend_smooth.index, s2_blend_smooth.values, label="SU neu")

    ax5.set_xlabel("Zeit (MESZ)")
    ax5.set_ylabel("Strahlung [W/m²]")
    #ax5.set_title("Sensor SU: gemessen vs. Ersatz (Cos-Blend) – Ersatzfenster hervorgehoben")
    ax5.set_ylim(bottom=0, top=1100  )

    _format_time_axis_mesz(ax5)
    _apply_zoom(ax5)
    ax5.grid(True, which="major", alpha=0.45)
    ax5.grid(True, which="minor", alpha=0.25)
    plt.setp(ax5.get_xticklabels(), rotation=55, ha="right")

    #style_meas2  = Line2D([0],[0], linestyle="-",  label="gemessen (geglättet)")
    style_blend2 = Line2D([0],[0], linestyle="-", color="orange" ,label="SU neu")
    patch_w2     = Patch(alpha=0.18, label="Zeitfenster in denen ersetzt wurde")
    ax5.legend(handles=[line_meas2, style_blend2, patch_w2], loc="best")

    #_note(ax5, "Analog zu S1: Ersatz nur in markierten Fenstern und an Tagen mit hoher S2-Korrelation zum Cosinus-Fit.")
    plt.tight_layout(); plt.show()

    # 6) Nur ERSATZ (S2)
    fig6, ax6 = plt.subplots(figsize=(12.5, 6.0))
    ax6.plot(s1_blend_smooth.index, s1_blend_smooth.values, label="SO neu")
    ax6.plot(s2_blend_smooth.index, s2_blend_smooth.values, label="SU neu")
    ax6.set_xlabel("Zeit (MESZ)")
    ax6.set_ylabel("Strahlung [W/m²]")
    #ax6.set_title("Sensor SU – Ersatz/Blend (10-min geglättet)")
    ax6.set_ylim(bottom=0, top=1100)

    _format_time_axis_mesz(ax6)
    _apply_zoom(ax6)
    ax6.grid(True, which="major", alpha=0.45)
    ax6.grid(True, which="minor", alpha=0.25)
    plt.setp(ax6.get_xticklabels(), rotation=55, ha="right")
    ax6.legend(loc="best")
    #_note(ax6, "Gezeigt wird ausschließlich die ersetzte/gebänderte Serie von S2.")
    plt.tight_layout(); plt.show()


if __name__ == "__main__":
    main()