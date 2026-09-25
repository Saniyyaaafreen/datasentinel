
import json
import sys
import pandas as pd


def check_types(file_path, schema_path):
    df = pd.read_csv(file_path)

    with open(schema_path, "r") as f:
        schema = json.load(f)

    results = {}

    for col, expected in schema.items():

        if col not in df.columns:
            results[col] = {
                "status": "MISSING COLUMN",
                "expected": expected,
                "actual": None
            }
            continue

        actual = str(df[col].dtype)

        ok = (
            (expected == "int" and "int" in actual) or
            (expected == "float" and (
                "float" in actual or "int" in actual
            )) or
            (expected == "string" and (
                "object" in actual or "string" in actual
            ))
        )

        if ok:
            results[col] = {
                "status": "OK",
                "expected": expected,
                "actual": actual
            }
        else:
            results[col] = {
                "status": "MISMATCH",
                "expected": expected,
                "actual": actual
            }

    return results


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(
            "Usage: python scripts/check_types.py data.csv schema.json"
        )
        sys.exit(1)

    file_path = sys.argv[1]
    schema_path = sys.argv[2]

    results = check_types(file_path, schema_path)

    print("\n========== TYPE CHECK ==========\n")

    for col, data in results.items():

        if data["status"] == "OK":
            print(f"{col}: OK")

        elif data["status"] == "MISSING COLUMN":
            print(f"{col}: MISSING COLUMN")

        else:
            print(
                f"{col}: MISMATCH "
                f"(expected {data['expected']}, "
                f"got {data['actual']})"
            )
