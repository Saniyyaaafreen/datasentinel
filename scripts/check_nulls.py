import sys
import pandas as pd


def check_nulls(file_path):
    df = pd.read_csv(file_path)

    total_rows = len(df)

    results = {}

    for column in df.columns:

        null_count = int(df[column].isnull().sum())

        if total_rows > 0:
            percentage = (
                null_count / total_rows
            ) * 100
        else:
            percentage = 0

        results[column] = {
            "missing_values": null_count,
            "percentage": round(float(percentage), 2),
            "warning": percentage > 10
        }

    return results


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/check_nulls.py data/yourfile.csv"
        )
        sys.exit(1)

    file_path = sys.argv[1]

    try:

        results = check_nulls(file_path)

        print(
            "\n========== NULL VALUE REPORT ==========\n"
        )

        for column, data in results.items():

            print(f"Column: {column}")
            print(
                f"Missing Values : "
                f"{data['missing_values']}"
            )
            print(
                f"Percentage     : "
                f"{data['percentage']:.2f}%"
            )

            if data["warning"]:
                print(
                    "⚠ WARNING: "
                    "More than 10% missing values!"
                )

            print("-" * 40)

    except FileNotFoundError:

        print(
            f"Error: File '{file_path}' not found."
        )

    except Exception as e:

        print(f"An error occurred: {e}")
