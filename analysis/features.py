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
CASES_FILE = BASE_DIR / "groundtruth" / "cases.csv"
OUTPUT_FILE = BASE_DIR / "analysis" / "features.csv"


# Nustatymai

SMOOTHING_WINDOW = 7


# Pagalbinės funkcijos

def load_cases():
    """Nuskaito cases.csv ir grąžina series_file -> label žemėlapį."""

    cases = pd.read_csv(CASES_FILE)

    required_columns = {"series_file", "label"}

    missing = required_columns - set(cases.columns)

    if missing:
        raise ValueError(
            f"cases.csv trūksta stulpelių: {', '.join(missing)}"
        )

    return dict(zip(cases["series_file"], cases["label"]))


def find_label(series_file, labels):
    """Suranda serijos label pagal failo pavadinimą."""

    # Paverčiame kelią į tokį pat formatą kaip cases.csv
    relative_path = series_file.relative_to(BASE_DIR).as_posix()

    if relative_path in labels:
        return labels[relative_path]

    # Atsarginis variantas: ieškome tik pagal failo pavadinimą
    for case_file, label in labels.items():
        case_name = Path(str(case_file).replace("\\", "/")).name

        if case_name == series_file.name:
            return label

    return None


def calculate_autocorrelation(series, lag):
    """Apskaičiuoja autokoreliaciją nurodytu vėlavimu."""

    if len(series) <= lag:
        return np.nan

    x = np.asarray(series[:-lag], dtype=float)
    y = np.asarray(series[lag:], dtype=float)

    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan

    return np.corrcoef(x, y)[0, 1]


def calculate_log_slope(series):
    """
    Apskaičiuoja tiesės nuolydį logaritmuotoje serijoje.

    Naudojamas ln(views + 1), kad nulinės reikšmės nesukeltų
    logaritmo klaidos.
    """

    y = np.log1p(np.asarray(series, dtype=float))
    x = np.arange(len(y))

    if len(y) < 2:
        return np.nan

    slope = np.polyfit(x, y, 1)[0]

    return slope


def count_peaks(series, baseline):
    """
    Suskaičiuoja atskirus reikšmingus pikus.

    Piku laikome lokalų maksimumą, kuris yra bent 1.5x
    bazinio lygio. Kad keli vienas šalia kito esantys taškai
    nebūtų laikomi atskirais pikais, tarp pikų turi būti bent
    7 dienos.
    """

    values = np.asarray(series, dtype=float)

    if len(values) < 3 or baseline <= 0:
        return 0

    threshold = baseline * 1.5

    peak_indices = []

    for i in range(1, len(values) - 1):

        is_peak = (
            values[i] > values[i - 1]
            and values[i] >= values[i + 1]
            and values[i] >= threshold
        )

        if not is_peak:
            continue

        # Jei pikas per arti ankstesnio, laikome tą patį įvykį.
        if peak_indices and i - peak_indices[-1] < 7:
            # Pasiliekame aukštesnį piką.
            if values[i] > values[peak_indices[-1]]:
                peak_indices[-1] = i
        else:
            peak_indices.append(i)

    return len(peak_indices)


def days_from_peak_to_return(series, baseline):
    """
    Randa didžiausią piką ir kiek dienų praeina,
    kol serija po piko grįžta iki 1.5x bazinio lygio.

    Jei negrįžta, grąžinama NaN.
    """

    values = np.asarray(series, dtype=float)

    if len(values) == 0 or baseline <= 0:
        return 0

    peak_index = int(np.argmax(values))
    threshold = baseline * 1.5

    # Ieškome tik po didžiausio piko.
    for i in range(peak_index + 1, len(values)):
        if values[i] <= threshold:
            return i - peak_index

    return 0


# Vienos serijos požymiai

def calculate_features(series_file, label):
    """Apskaičiuoja visus požymius vienai serijai."""

    df = pd.read_csv(series_file)

    if "date" not in df.columns or "views" not in df.columns:
        raise ValueError(
            f"{series_file} turi turėti 'date' ir 'views' stulpelius."
        )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["views"] = pd.to_numeric(df["views"], errors="coerce")

    df = df.dropna(subset=["date", "views"])
    df = df.sort_values("date")

    if df.empty:
        raise ValueError(f"Serija {series_file} yra tuščia.")

    views = df["views"].astype(float).to_numpy()

    # Triukšmo mažinimas

    smoothed = (
        pd.Series(views)
        .rolling(
            window=SMOOTHING_WINDOW,
            center=True,
            min_periods=1
        )
        .median()
        .to_numpy()
    )

    n = len(smoothed)

    # Pirmų ir paskutinių 90 dienų langai.
    first_90 = smoothed[:min(90, n)]
    last_90 = smoothed[max(0, n - 90):]

    baseline = float(np.median(first_90))
    final_level = float(np.median(last_90))

    # Apsauga nuo dalybos iš nulio.
    if baseline > 0:
        level_ratio = final_level / baseline
        peak_ratio = float(np.max(smoothed)) / baseline
        days_above_2x = int(np.sum(smoothed > 2 * baseline))
    else:
        level_ratio = np.nan
        peak_ratio = np.nan
        days_above_2x = 0

    # 1. Bazinis lygis
    baseline_feature = baseline

    # 2. Galutinis lygis
    final_level_feature = final_level

    # 3. Lygių santykis
    level_ratio_feature = level_ratio

    # 4. Didžiausias pikas / bazinis lygis
    peak_ratio_feature = peak_ratio

    # 5. Dienų virš 2x bazinio lygio
    days_above_2x_feature = days_above_2x

    # 6. Dienos nuo piko iki grįžimo į 1.5x bazinį lygį
    return_days_feature = days_from_peak_to_return(
        smoothed,
        baseline
    )

    # 7. Autokoreliacija ties 365 dienų vėlavimu
    autocorrelation_365_feature = calculate_autocorrelation(
        smoothed,
        365
    )

    # 8. Variacijos koeficientas
    mean = np.mean(smoothed)
    std = np.std(smoothed)

    if mean != 0:
        coefficient_variation = std / mean
    else:
        coefficient_variation = np.nan

    # 9. Logaritmuotos serijos nuolydis
    log_slope_feature = calculate_log_slope(smoothed)

    # 10. Atskirų pikų skaičius
    peak_count_feature = count_peaks(
        smoothed,
        baseline
    )

    # Rezultatas

    return {
        "series_file": str(series_file.relative_to(BASE_DIR)),
        "label": label,

        "baseline_90d": baseline_feature,
        "final_level_90d": final_level_feature,
        "level_ratio": level_ratio_feature,
        "peak_ratio": peak_ratio_feature,
        "days_above_2x_baseline": days_above_2x_feature,
        "days_peak_to_1.5x": return_days_feature,
        "autocorrelation_365d": autocorrelation_365_feature,
        "coefficient_variation": coefficient_variation,
        "log_slope": log_slope_feature,
        "peak_count": peak_count_feature,
    }


# Pagrindinė programa
def main():

    print("Nuskaitomas cases.csv...")

    labels = load_cases()

    series_files = sorted(SERIES_DIR.glob("*.csv"))

    if not series_files:
        raise FileNotFoundError(
            f"Nerasta CSV failų: {SERIES_DIR}"
        )

    print(f"Rasta serijų: {len(series_files)}")

    results = []

    for i, series_file in enumerate(series_files, start=1):

        print(
            f"[{i}/{len(series_files)}] "
            f"Skaičiuojama: {series_file.name}"
        )

        label = find_label(series_file, labels)

        if label is None:
            print(
                f"  ĮSPĖJIMAS: nerastas label "
                f"cases.csv faile."
            )

        try:
            features = calculate_features(
                series_file,
                label
            )

            results.append(features)

        except Exception as e:
            print(
                f"  KLAIDA apdorojant "
                f"{series_file.name}: {e}"
            )

    if not results:
        raise RuntimeError(
            "Nepavyko apskaičiuoti nė vienos serijos požymių."
        )

    result_df = pd.DataFrame(results)

    # Užtikriname, kad analysis katalogas egzistuoja.
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 60)
    print("BAIGTA")
    print("=" * 60)
    print(f"Rezultatas: {OUTPUT_FILE}")
    print(f"Serijų: {len(result_df)}")
    print()
    print("Požymiai:")

    feature_columns = [
        "baseline_90d",
        "final_level_90d",
        "level_ratio",
        "peak_ratio",
        "days_above_2x_baseline",
        "days_peak_to_1.5x",
        "autocorrelation_365d",
        "coefficient_variation",
        "log_slope",
        "peak_count",
    ]

    for column in feature_columns:
        print(f"  - {column}")


if __name__ == "__main__":
    main()