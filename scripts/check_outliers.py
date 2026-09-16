import sys
import pandas as pd


def check_outliers(file_path):
    df = pd.read_csv(file_path)

    results = {}

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for column in numeric_cols:
        mean = df[column].mean()
        std = df[column].std()

        if std == 0:
            continue

        lower_limit = mean - (3 * std)
        upper_limit = mean + (3 * std)

        outlier_rows = df[
            (df[column] < lower_limit) |
            (df[column] > upper_limit)
        ]

        results[column] = {
            "mean": round(float(mean), 2),
            "std_dev": round(float(std), 2),
            "lower_limit": round(float(lower_limit), 2),
            "upper_limit": round(float(upper_limit), 2),
            "outlier_count": int(len(outlier_rows)),
            "outlier_indices": [
                int(index) for index in outlier_rows.index
            ]
        }

    return results


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/check_outliers.py data/file.csv"
        )
        sys.exit(1)

    file_path = sys.argv[1]

    results = check_outliers(file_path)

    print("\n========== OUTLIER REPORT ==========\n")

    for column, data in results.items():
        print("Column:", column)
        print("Mean:", data["mean"])
        print("Std Dev:", data["std_dev"])
        print("Outliers:", data["outlier_count"])
        print(
            "Outlier indices:",
            data["outlier_indices"]
        )
        print("-" * 40)
