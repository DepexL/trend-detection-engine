# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "matplotlib"]
# ///

import requests
import csv
import os
import matplotlib.pyplot as plt


START_DATE = "20210701"
END_DATE = "20260630"

SERIES_DIR = "series"
CASES_FILE = "cases.csv"


def get_pageviews(article, start_date, end_date):
    """
    Gauna Wikipedia straipsnio dienos peržiūras.
    """

    article_url = article.replace(" ", "_")

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/"
        f"per-article/en.wikipedia/all-access/all-agents/"
        f"{article_url}/daily/{start_date}/{end_date}"
    )

    headers = {
        "User-Agent": "AI-Praktikantas/1.0 liutauraskuzma1@gmail.com"
    }

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    result = []

    for item in data["items"]:
        result.append({
            "date": item["timestamp"][:8],
            "views": item["views"]
        })

    return result


def save_series(article, data):
    """
    Išsaugo vieno Wikipedia straipsnio seriją CSV faile.
    """

    os.makedirs(SERIES_DIR, exist_ok=True)

    filename = article.replace(" ", "_") + ".csv"

    filepath = os.path.join(
        SERIES_DIR,
        filename
    )

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "date",
            "views"
        ])

        for item in data:
            date = item["date"]

            # API grąžina YYYYMMDD
            # Paverčiame į YYYY-MM-DD
            formatted_date = (
                f"{date[:4]}-{date[4:6]}-{date[6:8]}"
            )

            writer.writerow([
                formatted_date,
                item["views"]
            ])

    return filename


def plot_series(article, data):
    """
    Nupiešia Wikipedia peržiūrų grafiką.
    """

    dates = [
        item["date"]
        for item in data
    ]

    views = [
        item["views"]
        for item in data
    ]

    plt.figure(figsize=(14, 5))

    plt.plot(
        dates,
        views
    )

    plt.title(article)

    plt.xlabel("Data")
    plt.ylabel("Wikipedia peržiūros")

    # Kad nerodytų visų 1800 datų ant X ašies
    plt.xticks(
        dates[::180],
        rotation=45
    )

    plt.tight_layout()
    plt.show()


def save_case(
    article,
    series_file,
    label,
    why
):
    """
    Prideda vieną atvejį į cases.csv.
    """

    file_exists = os.path.exists(CASES_FILE)

    with open(
        CASES_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "article",
                "series_file",
                "period_start",
                "period_end",
                "label",
                "why"
            ])

        writer.writerow([
            article,
            series_file,
            "2021-07-01",
            "2026-06-30",
            label,
            why
        ])


if __name__ == "__main__":

    articles = [
        
    ]

    for article in articles:

        print(
            f"\nGaunami duomenys: {article}"
        )

        data = get_pageviews(
            article,
            START_DATE,
            END_DATE
        )

        print(
            f"Gauta dienų: {len(data)}"
        )

        series_file = save_series(
            article,
            data
        )

        plot_series(
            article,
            data
        )

        label = input(
            "Label (breakout/spike/seasonal/stable): "
        )

        why = input(
            "Why: "
        )

        save_case(
            article,
            series_file,
            label,
            why
        )