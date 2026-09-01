# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///


import pandas as pd
import numpy as np
from pathlib import Path


# Keliai

BASE_DIR = Path(__file__).resolve().parent.parent
SERIES_DIR = BASE_DIR / "groundtruth" / "series"


# Konstantos - taisyklių ribos (iš GROUNDTRUTH.md metodikos)

SMOOTHING_WINDOW = 7      # triukšmo mažinimui, sutampa su features.py
BASELINE_WINDOW = 90      # dienų langas baseline/final_level skaičiavimui
AUTOCORR_LAG = 365        # metinis vėlavimas sezoniškumui tikrinti

PEAK_RATIO_THRESHOLD = 3.0        # "3x bazinis lygis šuoliui"
RETURN_TO_BASELINE_RATIO = 1.5    # grįžimas prie baseline - skiria spike nuo breakout
AUTOCORR_SEASONAL_THRESHOLD = 0.5 # sezoniškumui reikia stipraus metinio pasikartojimo


# Pagalbinės funkcijos

def load_series(series_file):
    """Nuskaito seriją ir grąžina išlygintą (7d mediana) views masyvą."""

    df = pd.read_csv(series_file)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["views"] = pd.to_numeric(df["views"], errors="coerce")

    df = df.dropna(subset=["date", "views"])
    df = df.sort_values("date")

    if df.empty:
        raise ValueError(f"Serija {series_file} yra tuščia.")

    views = df["views"].astype(float).to_numpy()

    smoothed = (
        pd.Series(views)
        .rolling(window=SMOOTHING_WINDOW, center=True, min_periods=1)
        .median()
        .to_numpy()
    )

    return smoothed


def calculate_stats(smoothed):
    """Apskaičiuoja požymius, kurių reikia taisyklėms."""

    n = len(smoothed)

    first_window = smoothed[:min(BASELINE_WINDOW, n)]
    last_window = smoothed[max(0, n - BASELINE_WINDOW):]

    baseline = float(np.median(first_window))
    final_level = float(np.median(last_window))

    if baseline > 0:
        level_ratio = final_level / baseline
        peak_ratio = float(np.max(smoothed)) / baseline
    else:
        level_ratio = np.nan
        peak_ratio = np.nan

    autocorrelation = calculate_autocorrelation(smoothed, AUTOCORR_LAG)

    return {
        "baseline": baseline,
        "final_level": final_level,
        "level_ratio": level_ratio,
        "peak_ratio": peak_ratio,
        "autocorrelation": autocorrelation,
    }


def calculate_autocorrelation(series, lag):
    """Autokoreliacija nurodytu vėlavimu (metinis ciklas)."""

    if len(series) <= lag:
        return np.nan

    x = np.asarray(series[:-lag], dtype=float)
    y = np.asarray(series[lag:], dtype=float)

    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan

    return float(np.corrcoef(x, y)[0, 1])


def classify(stats):
    """
    Taisyklėmis paremtas klasifikatorius. Tvarka svarbi:

    1. Pirmiausia tikrinam sezoniškumą (metinę autokoreliaciją) - nes
       sezoniniai įvykiai (Kalėdos, Helovinas) irgi turi didelius pikus,
       ir jei tikrintume peak_ratio anksčiau, jie patektų į spike/breakout.
    2. Jei piko nėra (peak_ratio < 3x) - stable.
    3. Jei pikas yra, bet serija negrįžo prie baseline - breakout.
    4. Jei pikas yra ir serija grįžo prie baseline - spike.
    """

    if np.isnan(stats["autocorrelation"]) or np.isnan(stats["peak_ratio"]):
        return "stable"

    if stats["autocorrelation"] >= AUTOCORR_SEASONAL_THRESHOLD:
        return "seasonal"

    if stats["peak_ratio"] < PEAK_RATIO_THRESHOLD:
        return "stable"

    if stats["level_ratio"] >= RETURN_TO_BASELINE_RATIO:
        return "breakout"

    return "spike"


def classify_series(series_file):
    """Paima serijos CSV kelią, grąžina vieną iš keturių etikečių."""

    smoothed = load_series(series_file)
    stats = calculate_stats(smoothed)

    return classify(stats), stats


if __name__ == "__main__":
    # Greitas patikrinimas ant pirmos rastos serijos.
    series_files = sorted(SERIES_DIR.glob("*.csv"))

    if not series_files:
        raise FileNotFoundError(f"Nerasta CSV failų: {SERIES_DIR}")

    label, stats = classify_series(series_files[0])

    print(f"{series_files[0].name}: {label}")
    print(stats)
