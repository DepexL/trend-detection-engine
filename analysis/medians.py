# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///

from pathlib import Path
import pandas as pd

# analysis/medians.py -> projekto aplankas
BASE_DIR = Path(__file__).resolve().parent.parent

FEATURES_FILE = BASE_DIR / "analysis" / "features.csv"

df = pd.read_csv(FEATURES_FILE)

# Požymių stulpeliai, kuriems skaičiuosime medianą
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


# Mediana pagal klasę
medians = df.groupby("label")[feature_columns].median()

# Norima klasių tvarka
class_order = ["breakout", "spike", "seasonal", "stable"]

medians = medians.reindex(class_order)

print(medians.round(4).to_string())