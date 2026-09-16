import sys
import pandas as pd


def check_duplicates(file_path):
    df = pd.read_csv(file_path)

    exact_duplicates = df[df.duplicated()]

    results = {
        "total_rows": int(len(df)),
        "exact_duplicates": int(len(exact_duplicates)),
        "duplicate_indices": [
            int(index) for index in exact_duplicates.index
        ],
        "near_duplicate_count": None,
        "near_duplicate_check": "skipped"
    }

    if "user_id" in df.columns and "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        df = df.sort_values(
            ["user_id", "timestamp"]
        )

        df["time_diff"] = (
            df.groupby("user_id")["timestamp"]
            .diff()
            .dt.total_seconds()
        )

        near_duplicates = df[
            (df["time_diff"] > 0) &
            (df["time_diff"] <= 300)
        ]

        results["near_duplicate_count"] = int(
            len(near_duplicates)
        )

        results["near_duplicate_check"] = "performed"

    return results


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/check_duplicates.py data.csv"
        )
        sys.exit(1)

    file_path = sys.argv[1]

    results = check_duplicates(file_path)

    print("\n========== DUPLICATE REPORT ==========\n")

    print(
        f"Total rows: {results['total_rows']}"
    )

    print(
        f"Exact duplicate rows: "
        f"{results['exact_duplicates']}"
    )

    if results["near_duplicate_check"] == "performed":

        print(
            f"Near duplicates (within 5 minutes): "
            f"{results['near_duplicate_count']}"
        )

    else:

        print(
            "Near duplicate check skipped "
            "(user_id/timestamp not found)."
        )
