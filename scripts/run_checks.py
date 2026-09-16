import json
import sys

import pandas as pd

from check_nulls import check_nulls
from check_outliers import check_outliers
from check_types import check_types
from check_duplicates import check_duplicates
from ai_explainer import explain_flagged_row


if len(sys.argv) != 3:
    print(
        "Usage: python scripts/run_checks.py data.csv schema.json"
    )
    sys.exit(1)


file_path = sys.argv[1]
schema_path = sys.argv[2]


print(
    "\n========== FULL DATA QUALITY PIPELINE ==========\n"
)


# -------------------------
# Run validation checks
# -------------------------

print("--- NULL CHECK ---")
null_results = check_nulls(file_path)
print("Null check completed.\n")


print("--- OUTLIER CHECK ---")
outlier_results = check_outliers(file_path)
print("Outlier check completed.\n")


print("--- TYPE CHECK ---")
type_results = check_types(
    file_path,
    schema_path
)
print("Type check completed.\n")


print("--- DUPLICATE CHECK ---")
duplicate_results = check_duplicates(file_path)
print("Duplicate check completed.\n")


# -------------------------
# AI EXPLANATION LAYER
# -------------------------

print("--- AI EXPLANATION LAYER ---")

df = pd.read_csv(file_path)

ai_explanations = []

for column, data in outlier_results.items():

    if data["outlier_count"] == 0:
        continue

    lower_limit = data["lower_limit"]
    upper_limit = data["upper_limit"]

    for pandas_index in data["outlier_indices"]:

        # Get the complete flagged row
        row = df.iloc[pandas_index].to_dict()

        # Get the suspicious value
        value = row[column]

        # Determine the exact validation reason
        if value < lower_limit:

            reason = (
                f"{column} value {value} is below "
                f"the DataSentinel lower limit of "
                f"{lower_limit}"
            )

        else:

            reason = (
                f"{column} value {value} is above "
                f"the DataSentinel upper limit of "
                f"{upper_limit}"
            )

        # Convert pandas index to human-readable row number
        row_number = pandas_index + 1

        print(
            f"Generating explanation for "
            f"row {row_number}, column '{column}'..."
        )

        try:

            explanation = explain_flagged_row(
                row_dict=row,
                row_index=row_number,
                flag_reason=reason
            )

            ai_explanations.append(
                {
                    "pandas_index": int(pandas_index),
                    "row_number": int(row_number),
                    "column": column,
                    "value": value,
                    "validation_reason": reason,
                    "ai_explanation": explanation,
                    "status": "SUCCESS"
                }
            )

        except Exception as e:

            print(
                f"AI explanation failed for "
                f"row {row_number}, column '{column}': {e}"
            )

            ai_explanations.append(
                {
                    "pandas_index": int(pandas_index),
                    "row_number": int(row_number),
                    "column": column,
                    "value": value,
                    "validation_reason": reason,
                    "ai_explanation": None,
                    "status": "ERROR"
                }
            )


print(
    f"\nAI explanations generated: "
    f"{len(ai_explanations)}"
)


# -------------------------
# Combine all results
# -------------------------

results = {
    "file": file_path,
    "nulls": null_results,
    "outliers": outlier_results,
    "types": type_results,
    "duplicates": duplicate_results,
    "ai_explanations": ai_explanations
}


# -------------------------
# Save results
# -------------------------

output_file = "reports/results.json"

with open(output_file, "w") as f:

    json.dump(
        results,
        f,
        indent=4
    )


print(
    f"\nResults saved to: {output_file}"
)

print(
    "\n========== ALL CHECKS + AI COMPLETED ==========\n"
)

# -------------------------
# Generate HTML report
# -------------------------

print("--- GENERATING HTML REPORT ---")

import subprocess

subprocess.run(
    ["python", "scripts/generate_report.py", file_path],
    check=True
)

print("\n========== FULL PIPELINE COMPLETED ==========\n")
