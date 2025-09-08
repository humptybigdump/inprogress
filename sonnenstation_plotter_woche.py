# -*- coding: utf-8 -*-
"""
CSV + LOG PIPELINE (Sonne & Felix) – mit intelligenter Lücken-Interpolation

Neu:
- Interpolation von NaN-Lücken mittels "Zeit-des-Tages"-Vorlage (Median über alle Tage),
  angepasst an die Randpunkte der Lücke (a*Template + b).
- Alle interpolierten Punkte werden in Exporten markiert (Flag_S1 / Flag_S2 = "interpol").

Bestehendes bleibt:
- CSVs + LOGs (auch dateiendungslos *mosquitto-sub*ufp*), Zeitzone Europe/Berlin.
- Priorität: bis 13.08.2025 15:22:00 Sonne; ab 13.08.2025 15:22:57 Felix.
- Felix-Skalierung: S1 × 2.0325203252, S2 × 2.01207243461 (CSV & LOG).
- Plot nur geglättet (10 min), Lücken >5 min schattiert.
- Zeitachse im Plot: NUR 12:00 (MESZ) als beschrifteter Major-Tick, 00:00 (MESZ) als unbeschrifteter Minor-Tick.
- Exporte ab 04.08.2025 00:00 MESZ:
    1) merged_sensor12_from_2025-08-04.csv (unglättet + Flags)
    2) merged_10min_means_from_2025-08-04_every_10min.csv (unglättet + Flags)
"""

from __future__ import annotations
import re, csv
from pathlib import Path
from typing import Tuple, Optional, List, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
from zoneinfo import ZoneInfo

# ====================== CONFIG ======================
INPUT_DIR = Path(r"C:\Leon Dietrich\UNI\Feldpraktikum daten\Sonnebearbeitet") #Hier bitte Ihren Pfad mit den Dateien (Felix und Sonnenstation) einfügen.
TZ = ZoneInfo("Europe/Berlin")
START_AT  = pd.Timestamp(2025, 8, 4, 0, 0, tz=TZ)

# Zeit-Umschaltung:
SWITCH_TIME_SONNE_END   = pd.Timestamp(2025, 8, 13, 15, 22, 0, tz=TZ)   # bis inkl. hier: Sonne bevorzugt
SWITCH_TIME_FELIX_START = pd.Timestamp(2025, 8, 13, 15, 22, 57, tz=TZ)  # ab hier: Felix bevorzugt

# Matching / Plot
TOLERANCE_SECONDS   = 10      # nearest-match Toleranz für CSV/LOG
GAP_MINUTES         = 5       # Lückenschwelle für Markierung/Schraffur
PLOT_SMOOTH_MINUTES = 10      # Glättung NUR im Plot

# Kalibrierungsfaktoren (Felix)
FELIX_S1_FACTOR = 2.0325203252
FELIX_S2_FACTOR = 2.01207243461

# Export-Dateien
OUTPUT_FILENAME_RAW   = "merged_sensor12_from_2025-08-04.csv"
OUTPUT_FILENAME_10MIN = "merged_10min_means_from_2025-08-04_every_10min.csv"
OUTPUT_DELIMITER = ","
# ====================================================

# ----------- CSV-Reader (robust) -----------
def _sniff_delim_and_decimal(p: Path) -> Tuple[str, str]:
    sample = p.read_text(encoding="utf-8", errors="ignore")[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
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
    for k in ["zeitstempel", "zeit", "time", "timestamp", "datetime", "datum", "date"]:
        if k in low:
            return low[k]
    return df.columns[0]

def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s.strip().lower())

def _pick_col_from_aliases(df: pd.DataFrame, aliases: List[str]) -> Optional[str]:
    df.columns = df.columns.str.strip()
    normmap = {_norm(c): c for c in df.columns}
    for a in aliases:
        na = _norm(a)
        if na in normmap:
            return normmap[na]
    return None

def _read_file_strict(p: Path) -> pd.DataFrame:
    sep, decimal = _sniff_delim_and_decimal(p)
    df = pd.read_csv(p, sep=sep, decimal=decimal, engine="python")
    if df.empty:
        raise ValueError(f"Datei leer: {p.name}")
    df.columns = df.columns.str.strip()

    ts_col = _find_timestamp_col(df)
    ts = _to_berlin(df[ts_col])

    s1_col = _pick_col_from_aliases(df, ["Strahlungsmittel_S1mittel", "Strahlung_S1mittel", "Strahlung_S1"])
    s2_col = _pick_col_from_aliases(df, ["Strahlungsmittel_S2mittel", "Strahlung_S2mittel", "Strahlung_S2"])

    missing = []
    if s1_col is None: missing.append("Strahlungsmittel_S1mittel | Strahlung_S1mittel | Strahlung_S1")
    if s2_col is None: missing.append("Strahlungsmittel_S2mittel | Strahlung_S2mittel | Strahlung_S2")
    if missing:
        raise ValueError(
            f"In '{p.name}' fehlen Pflichtspalten (auch nach Trim): {missing}. "
            f"Vorhandene Spalten: {list(df.columns)}"
        )

    s1 = pd.to_numeric(df[s1_col], errors="coerce")
    s2 = pd.to_numeric(df[s2_col], errors="coerce")

    print(f"{p.name}: Sensor1 <- '{s1_col}', Sensor2 <- '{s2_col}'")

    out = pd.DataFrame({"timestamp": ts, "sensor1": s1, "sensor2": s2})
    out = out.dropna(subset=["timestamp"]).sort_values("timestamp").drop_duplicates(subset=["timestamp"])
    return out

def _pick_files(folder: Path) -> Tuple[Path, Path]:
    csvs = sorted(folder.glob("*.csv"))
    if len(csvs) < 2:
        raise FileNotFoundError(f"Weniger als zwei CSV-Dateien in {folder}")
    felix = [p for p in csvs if "felix" in p.name.lower()]
    sonne = [p for p in csvs if "sonnen" in p.name.lower() or "sonne" in p.name.lower()]
    if felix and sonne:
        return sonne[0], felix[0]
    return csvs[0], csvs[1]

# ---------- Kalibrierung ----------
def _apply_felix_calibration(df: pd.DataFrame, label: str = "Felix") -> pd.DataFrame:
    df = df.copy()
    before1 = df["sensor1"].astype(float)
    before2 = df["sensor2"].astype(float)
    df["sensor1"] = before1 * FELIX_S1_FACTOR
    df["sensor2"] = before2 * FELIX_S2_FACTOR
    # Konsolencheck
    m1b = float(np.nanmedian(before1)) if np.isfinite(np.nanmedian(before1)) else np.nan
    m1a = float(np.nanmedian(df["sensor1"])) if np.isfinite(np.nanmedian(df["sensor1"])) else np.nan
    m2b = float(np.nanmedian(before2)) if np.isfinite(np.nanmedian(before2)) else np.nan
    m2a = float(np.nanmedian(df["sensor2"])) if np.isfinite(np.nanmedian(df["sensor2"])) else np.nan
    print(f"[Kalibrierung {label}] S1 × {FELIX_S1_FACTOR}  Median: {m1b:.3f} -> {m1a:.3f} | "
          f"S2 × {FELIX_S2_FACTOR}  Median: {m2b:.3f} -> {m2a:.3f}")
    return df

# ----------- LOG-Reader -----------
LOG_LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+0000)\s+"
    r"ufp/(?P<station>Sonnenstation|Felix)/Sensor_(?P<sensor>[12])/"
    r"(?P<field>strahlung)\s+(?P<val>[-+]?\d+(?:\.\d+)?)\s+W/m2\s*$"
)

def _parse_log_file(p: Path) -> List[Dict]:
    rows = []
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = LOG_LINE_RE.match(line.strip())
            if not m:
                continue
            ts_utc = pd.to_datetime(m.group("ts"), utc=True)
            ts = ts_utc.tz_convert(TZ)
            station = m.group("station")
            sensor = int(m.group("sensor"))
            val = float(m.group("val"))
            rows.append({"timestamp": ts, "station": station, "sensor": sensor, "value": val})
    return rows

def _read_logs(folder: Path) -> pd.DataFrame:
    """
    Liest LOG-Dateien:
      - *.log, *.txt
      - dateiendungslos wie: *mosquitto-sub*ufp*  (z. B. 20250811031820-mosquitto-sub-co2server-ufp)
    Sucht rekursiv in Unterordnern.
    """
    all_rows: List[Dict] = []
    seen = set()
    patterns = ("*.log", "*.txt", "*mosquitto-sub*ufp*")
    for pattern in patterns:
        for p in folder.rglob(pattern):
            if not p.is_file():
                continue
            real = p.resolve()
            if real in seen:
                continue
            seen.add(real)
            all_rows.extend(_parse_log_file(p))
    if not all_rows:
        return pd.DataFrame(columns=["timestamp","station","sensor","value"])
    df = pd.DataFrame(all_rows).sort_values("timestamp")
    df = df[df["timestamp"] >= START_AT].copy()
    return df

def _pivot_logs(df_logs: pd.DataFrame, station_name: str) -> pd.DataFrame:
    df = df_logs[df_logs["station"] == station_name].copy()
    if df.empty:
        return pd.DataFrame(columns=["timestamp","sensor1","sensor2"])
    wide = df.pivot_table(index="timestamp", columns="sensor", values="value", aggfunc="mean")
    wide = wide.rename(columns={1: "sensor1", 2: "sensor2"}).reset_index().sort_values("timestamp")
    return wide

# ----------- Interpolation (Zeit-des-Tages-Template) -----------
def _tod_template(series: pd.Series, bin_freq: str = "5T") -> pd.Series:
    """Median pro 5-Minuten-Tageszeit über alle Tage."""
    idx = series.index
    key = idx.floor(bin_freq).time
    df = pd.DataFrame({"val": series.values}, index=idx)
    df["key"] = key
    climo = df.groupby("key")["val"].median()
    return climo  # index: time objects

def _interpolate_with_template(series: pd.Series, climo: pd.Series, bin_freq: str = "5T") -> tuple[pd.Series, pd.Series]:
    """
    Füllt NaN-Blöcke in 'series' mithilfe eines Tageszeit-Templates 'climo'
    (Median pro 5-Minuten-Slot). An den Lückenrändern wird eine lineare
    Transformation a*Template+b ermittelt, sodass die Ränder exakt passen.
    Rückgabe: (gefüllte Serie, Flag-Serie (bool) für interpolierte Punkte)
    """
    s = series.copy()
    flags = pd.Series(False, index=s.index)

    # Template-Werte entlang der Achse
    keys = s.index.floor(bin_freq).time
    tmpl = pd.Series([climo.get(k, np.nan) for k in keys], index=s.index)

    vals = s.values
    idx = s.index

    # NaN-Blöcke finden
    isna = pd.isna(vals)
    if not isna.any():
        return s, flags

    blocks = []
    start = None
    for i, na in enumerate(isna):
        if na and start is None:
            start = i
        if (not na) and (start is not None):
            blocks.append((start, i-1)); start = None
    if start is not None:
        blocks.append((start, len(vals)-1))

    for i0, i1 in blocks:
        prev_idx = i0-1
        while prev_idx >= 0 and pd.isna(vals[prev_idx]): prev_idx -= 1
        next_idx = i1+1
        while next_idx < len(vals) and pd.isna(vals[next_idx]): next_idx += 1

        c_prev = tmpl.iloc[prev_idx] if prev_idx >= 0 else np.nan
        c_next = tmpl.iloc[next_idx] if next_idx < len(vals) else np.nan
        y_prev = vals[prev_idx] if prev_idx >= 0 else np.nan
        y_next = vals[next_idx] if next_idx < len(vals) else np.nan

        if np.isfinite(c_prev) and np.isfinite(c_next) and (c_next != c_prev):
            a = (y_next - y_prev) / (c_next - c_prev)
            b = y_prev - a*c_prev
            fill_vals = a*tmpl.iloc[i0:i1+1] + b
        elif np.isfinite(c_prev) and c_prev != 0:
            a = y_prev / c_prev; b = 0.0
            fill_vals = a*tmpl.iloc[i0:i1+1] + b
        elif np.isfinite(c_next) and c_next != 0:
            a = y_next / c_next; b = 0.0
            fill_vals = a*tmpl.iloc[i0:i1+1] + b
        else:
            if prev_idx >= 0 and next_idx < len(vals):
                t0 = (idx[i0:i1+1] - idx[prev_idx]).total_seconds()
                T  = (idx[next_idx] - idx[prev_idx]).total_seconds()
                frac = t0 / T
                fill_vals = y_prev + frac*(y_next - y_prev)
            else:
                fill_vals = tmpl.iloc[i0:i1+1]

        s.iloc[i0:i1+1] = fill_vals.values
        flags.iloc[i0:i1+1] = True

    return s, flags

# ----------- Helfer -----------
def _prefer_series(series_by_src: Dict[str, pd.Series], order: List[str]) -> pd.Series:
    out = pd.Series(np.nan, index=next(iter(series_by_src.values())).index, dtype="float64")
    for src in order:
        if src in series_by_src:
            out = out.where(~out.isna(), series_by_src[src])
    return out

# ====================== MAIN ======================
def main():
    # CSV-Dateien
    sonne_path, felix_path = _pick_files(INPUT_DIR)
    print(f"CSV gefunden:\n  Sonne: {sonne_path.name}\n  Felix: {felix_path.name}")

    df_sonne = _read_file_strict(sonne_path)
    df_felix = _read_file_strict(felix_path)
    df_felix = _apply_felix_calibration(df_felix, label="Felix-CSV")

    # Startfilter
    df_sonne = df_sonne[df_sonne["timestamp"] >= START_AT].copy()
    df_felix = df_felix[df_felix["timestamp"] >= START_AT].copy()
    if df_sonne.empty and df_felix.empty:
        raise ValueError("Keine CSV-Daten nach dem Startdatum in beiden Dateien.")

    # Union-Timeline aus CSVs
    union_ts = pd.Index(sorted(pd.unique(pd.concat([df_sonne["timestamp"], df_felix["timestamp"]]))))
    timeline = pd.DataFrame({"timestamp": union_ts})
    tol = pd.Timedelta(seconds=TOLERANCE_SECONDS)

    # As-of CSV-Merge
    m_sonne = pd.merge_asof(timeline[["timestamp"]], df_sonne.sort_values("timestamp"),
                            on="timestamp", direction="nearest", tolerance=tol)
    m_felix = pd.merge_asof(timeline[["timestamp"]], df_felix.sort_values("timestamp"),
                            on="timestamp", direction="nearest", tolerance=tol)

    # CSV-Quellenreihen (Präferenz vor/nach Schaltzeiten)
    csv_s1_before = _prefer_series({"sonne": m_sonne["sensor1"], "felix": m_felix["sensor1"]}, ["sonne", "felix"])
    csv_s2_before = _prefer_series({"sonne": m_sonne["sensor2"], "felix": m_felix["sensor2"]}, ["sonne", "felix"])
    csv_s1_after  = _prefer_series({"felix": m_felix["sensor1"], "sonne": m_sonne["sensor1"]}, ["felix", "sonne"])
    csv_s2_after  = _prefer_series({"felix": m_felix["sensor2"], "sonne": m_sonne["sensor2"]}, ["felix", "sonne"])

    merged = timeline.copy()
    mask_before  = merged["timestamp"] <= SWITCH_TIME_SONNE_END
    mask_after   = merged["timestamp"] >= SWITCH_TIME_FELIX_START
    mask_between = (~mask_before) & (~mask_after)  # konservativ Sonne

    merged["sensor1"] = np.where(mask_after, csv_s1_after, csv_s1_before)
    merged["sensor2"] = np.where(mask_after, csv_s2_after, csv_s2_before)
    merged.loc[mask_between, "sensor1"] = csv_s1_before[mask_between]
    merged.loc[mask_between, "sensor2"] = csv_s2_before[mask_between]

    # ---------- LOG-Füllung der NaN-Stellen ----------
    logs_df = _read_logs(INPUT_DIR)
    if not logs_df.empty:
        print(f"LOG-Zeilen gelesen: {len(logs_df)}")

        log_sonne = _pivot_logs(logs_df, "Sonnenstation")
        log_felix = _pivot_logs(logs_df, "Felix")
        if not log_felix.empty:
            log_felix = _apply_felix_calibration(log_felix, label="Felix-LOG")

        def asof_log(src: pd.DataFrame, s1name: str, s2name: str) -> pd.DataFrame:
            if src.empty:
                return timeline.assign(**{s1name: np.nan, s2name: np.nan})
            out = pd.merge_asof(timeline[["timestamp"]], src.sort_values("timestamp"),
                                on="timestamp", direction="nearest", tolerance=tol)
            return out.rename(columns={"sensor1": s1name, "sensor2": s2name})

        mlog_sonne = asof_log(log_sonne, "log_sonne_s1", "log_sonne_s2")
        mlog_felix = asof_log(log_felix, "log_felix_s1", "log_felix_s2")

        for col, sson, sfel in [
            ("sensor1", "log_sonne_s1", "log_felix_s1"),
            ("sensor2", "log_sonne_s2", "log_felix_s2"),
        ]:
            na_mask = merged[col].isna()
            fill_before = na_mask & (mask_before | mask_between)
            merged.loc[fill_before, col] = mlog_sonne[sson][fill_before]
            still_na = merged[col].isna() & (mask_before | mask_between)
            merged.loc[still_na, col] = mlog_felix[sfel][still_na]
            fill_after = merged[col].isna() & mask_after
            merged.loc[fill_after, col] = mlog_felix[sfel][fill_after]
            still_na2 = merged[col].isna() & mask_after
            merged.loc[still_na2, col] = mlog_sonne[sson][still_na2]

    # ---------- INTELLIGENTE INTERPOLATION (nur wo noch NaN) ----------
    merged = merged.sort_values("timestamp").reset_index(drop=True)
    ts_idx = merged["timestamp"]
    df_ts = merged.set_index("timestamp")[["sensor1", "sensor2"]]

    # Template aus allen Tagen (Median je 5-Minuten-Slot)
    climo_s1 = _tod_template(df_ts["sensor1"])
    climo_s2 = _tod_template(df_ts["sensor2"])

    filled_s1, flag_s1 = _interpolate_with_template(df_ts["sensor1"], climo_s1)
    filled_s2, flag_s2 = _interpolate_with_template(df_ts["sensor2"], climo_s2)

    filled = pd.DataFrame({"sensor1": filled_s1, "sensor2": filled_s2}, index=df_ts.index)
    flags  = pd.DataFrame({"Flag_S1": flag_s1, "Flag_S2": flag_s2}, index=df_ts.index)

    # ---------- EXPORT 1: Roh (mit Flags), Lückenstart weiterhin als NaT markieren ----------
    diffs = ts_idx.diff()
    gap_mask = diffs > pd.Timedelta(minutes=GAP_MINUTES)

    export_df = filled.reset_index().rename(columns={"index": "timestamp"})
    # WICHTIG: Flags vor Merge korrekt benennen
    flags_reset = flags.reset_index().rename(columns={"index": "timestamp"})
    export_df = export_df.merge(flags_reset, on="timestamp", how="left")

    export_df.loc[gap_mask.values, "timestamp"] = pd.NaT  # Marker für echte Zeitlücken
    export_df["Flag_S1"] = np.where(export_df["Flag_S1"], "interpol", "")
    export_df["Flag_S2"] = np.where(export_df["Flag_S2"], "interpol", "")
    export_df = export_df[(export_df["timestamp"].isna()) | (export_df["timestamp"] >= START_AT)]

    export_df_out = export_df.rename(columns={
        "sensor1": "Strahlungsmittel_S1mittel",
        "sensor2": "Strahlungsmittel_S2mittel"
    })[["timestamp", "Strahlungsmittel_S1mittel", "Strahlungsmittel_S2mittel", "Flag_S1", "Flag_S2"]]

    out1 = INPUT_DIR / OUTPUT_FILENAME_RAW
    export_df_out.to_csv(out1, index=False, sep=OUTPUT_DELIMITER)
    print(f"Export (roh) mit Flags geschrieben: {out1.resolve()}  (Zeilen: {len(export_df_out)})")

    # ---------- EXPORT 2: 10-Minuten-Mittel (mit Flags) ----------
    ts_df = filled[(~filled.index.isna()) & (filled.index >= START_AT)]

    try:
        resampled = ts_df.resample("10T", origin=START_AT, label="left", closed="left").mean(numeric_only=True)
    except TypeError:
        resampled = ts_df.resample("10T", origin=START_AT, label="left", closed="left").mean()

    flag10 = flags[(~flags.index.isna()) & (flags.index >= START_AT)].resample(
        "10T", origin=START_AT, label="left", closed="left"
    ).max().astype(bool)

    last_time = START_AT if len(ts_df.index) == 0 else ts_df.index.max().ceil("10T")
    fixed_index = pd.date_range(start=START_AT, end=last_time, freq="10T", tz=TZ)
    resampled = resampled.reindex(fixed_index)
    flag10 = flag10.reindex(fixed_index).fillna(False)

    export_10min = resampled.rename(columns={
        "sensor1": "Strahlungsmittel_S1mittel",
        "sensor2": "Strahlungsmittel_S2mittel"
    }).reset_index().rename(columns={"index": "timestamp"})

    export_10min["Flag_S1"] = np.where(flag10["Flag_S1"].values, "interpol", "")
    export_10min["Flag_S2"] = np.where(flag10["Flag_S2"].values, "interpol", "")

    out2 = INPUT_DIR / OUTPUT_FILENAME_10MIN
    export_10min.to_csv(out2, index=False, sep=OUTPUT_DELIMITER)
    print(f"Export (10-min-Mittel) mit Flags geschrieben: {out2.resolve()}  (Zeilen: {len(export_10min)})")

    # ---------- PLOT (nur Darstellung; basiert auf 'filled', aber Lücken schattieren) ----------
    plot_df = filled.copy()
    # Bruchstellen für Rolling trennen, damit Glättung nicht über echte Lücken "brückt"
    break_mask = plot_df.index.to_series().diff() > pd.Timedelta(minutes=GAP_MINUTES)
    for col in ["sensor1", "sensor2"]:
        plot_df.loc[break_mask, col] = np.nan

    smooth = plot_df.rolling(f"{PLOT_SMOOTH_MINUTES}min", min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(12.5, 6.2))  # Fix: sinnvolle Höhe
    ax.plot(smooth.index, smooth["sensor1"], label="SO")
    ax.plot(smooth.index, smooth["sensor2"], label="SU")

    ax.set_xlabel("Zeit (MESZ)")
    ax.set_ylabel("Strahlung (W/m²)")
    #ax.set_title("gemessene Strahlungswerte der Sonnenstation – 10-min geglättet")

    # Nur 12:00 (MESZ) als beschrifteter Major-Tick; 00:00 als unbeschrifteter Minor-Tick
    ax.xaxis.set_major_locator(HourLocator(byhour=[12], tz=TZ))
    ax.xaxis.set_minor_locator(HourLocator(byhour=[0],  tz=TZ))
    ax.xaxis.set_major_formatter(DateFormatter("%d.%m. %H:%M", tz=TZ))

    ax.grid(True, which="major", alpha=0.4)
    ax.grid(True, which="minor", alpha=0.2)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    ax.legend(loc="best")

    # Lücken schattieren (echte Zeitlücken > 5 min – unabhängig von Interpolation)
    ts_idx_sorted = ts_idx.sort_values().reset_index(drop=True)
    for i in range(1, len(ts_idx_sorted)):
        t0, t1 = ts_idx_sorted[i-1], ts_idx_sorted[i]
        if pd.isna(t0) or pd.isna(t1):
            continue
        if (t1 - t0) > pd.Timedelta(minutes=GAP_MINUTES):
            ax.axvspan(t0, t1, alpha=0.25, zorder=0)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
