# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy", "scikit-learn"]
# ///

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)



# KELIAI


BASE_DIR = Path(__file__).resolve().parent.parent

CASES_FILE = BASE_DIR / "groundtruth" / "cases.csv"
SERIES_DIR = BASE_DIR / "groundtruth" / "series"
BASELINE_FILE = BASE_DIR / "analysis" / "BASELINE.md"



sys.path.insert(0, str(Path(__file__).resolve().parent))

from baseline import classify_series

# NUSTATYMAI


CLASSES = [
    "breakout",
    "spike",
    "seasonal",
    "stable",
]


# PAGALBINĖ FUNKCIJA


def resolve_series_path(series_path):
    path_string = str(series_path).replace("\\", "/")
    path = Path(path_string)

    if path.is_absolute():
        return path

    if path.parts[:2] == ("groundtruth", "series"):
        return BASE_DIR / path

    return SERIES_DIR / path.name




# PAGRINDINĖ PROGRAMA


def main():

    print("Nuskaitomas cases.csv...")

    cases = pd.read_csv(CASES_FILE)

    required_columns = {
        "article",
        "series_file",
        "label",
    }

    missing = required_columns - set(cases.columns)

    if missing:
        raise ValueError(
            "cases.csv trūksta stulpelių: "
            + ", ".join(missing)
        )

    true_labels = []
    predicted_labels = []

    mistakes = []

    print(f"Vertinama atvejų: {len(cases)}")
    print()

    # KLASIFIKUOJAME VISUS ATVEJUS

    for index, row in cases.iterrows():

        article = row["article"]
        actual_label = row["label"]

        series_file = resolve_series_path(
            row["series_file"]
        )

        print(
            f"[{index + 1}/{len(cases)}] "
            f"{article}"
        )

        if not series_file.exists():

            print(
                f"  KLAIDA: nerastas failas "
                f"{series_file}"
            )

            continue

        try:

            predicted_label, stats = classify_series(
                series_file
            )

            true_labels.append(actual_label)
            predicted_labels.append(predicted_label)

            print(
                f"  Tikra: {actual_label} | "
                f"Prognozė: {predicted_label}"
            )

            # Jei suklydo - išsaugome informaciją

            if predicted_label != actual_label:

                mistakes.append({
                    "article": article,
                    "actual": actual_label,
                    "predicted": predicted_label,
                    "stats": stats,
                })

        except Exception as error:

            print(
                f"  KLAIDA klasifikuojant: "
                f"{error}"
            )

    # PATIKRINAME, AR TURIME REZULTATŲ

    if not true_labels:

        raise RuntimeError(
            "Nepavyko suklasifikuoti nė vieno atvejo."
        )

    # ACCURACY

    accuracy = accuracy_score(
        true_labels,
        predicted_labels
    )

    # CONFUSION MATRIX

    matrix = confusion_matrix(
        true_labels,
        predicted_labels,
        labels=CLASSES
    )

    # SPAUSDINAME REZULTATUS

    print()

    print("BASELINE RESULTS")


    print()
    print(
        f"Accuracy: {accuracy:.4f} "
        f"({accuracy * 100:.2f}%)"
    )

    print()
    print("Confusion matrix:")
    print(matrix)

    print()
    print("Classification report:")

    print(
        classification_report(
            true_labels,
            predicted_labels,
            labels=CLASSES,
            zero_division=0
        )
    )

    print()
    print(
        f"Klaidingai suklasifikuota: "
        f"{len(mistakes)}"
    )


if __name__ == "__main__":
    main()