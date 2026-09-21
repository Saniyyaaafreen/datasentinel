import json
import os
import pandas as pd

from check_nulls import check_nulls
from check_outliers import check_outliers
from check_types import check_types
from check_duplicates import check_duplicates


def run_pipeline(file_path, schema_path, output_folder, ai_enabled=False):

    print(
        "\n========== FULL DATA QUALITY PIPELINE ==========\n"
    )

    # Create output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # --------------------------------
    # NULL CHECK
    # --------------------------------

    print("--- NULL CHECK ---")
    null_results = check_nulls(file_path)
    print("Null check completed.\n")

    # --------------------------------
    # OUTLIER CHECK
    # --------------------------------

    print("--- OUTLIER CHECK ---")
    outlier_results = check_outliers(file_path)
    print("Outlier check completed.\n")

    # --------------------------------
    # TYPE CHECK
    # --------------------------------

    print("--- TYPE CHECK ---")
    type_results = check_types(
        file_path,
        schema_path
    )
    print("Type check completed.\n")

    # Stop pipeline if required schema columns are missing
    missing_columns = [
        column
        for column, data in type_results.items()
        if data["status"] == "MISSING COLUMN"
    ]

    if missing_columns:
        raise ValueError(
            "Column mismatch. Missing required columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------
    # DUPLICATE CHECK
    # --------------------------------

    print("--- DUPLICATE CHECK ---")
    duplicate_results = check_duplicates(file_path)
    print("Duplicate check completed.\n")

    # --------------------------------
    # AI LAYER
    # --------------------------------

    ai_explanations = []
    ai_summary = None

    if ai_enabled:

        from ai_explainer import (
            explain_flagged_row,
            generate_dataset_summary
        )

        print("--- AI EXPLANATION LAYER ---")

        df = pd.read_csv(file_path)

        for column, data in outlier_results.items():

            if data["outlier_count"] == 0:
                continue

            lower_limit = data["lower_limit"]
            upper_limit = data["upper_limit"]

            for pandas_index in data["outlier_indices"]:

                row = df.iloc[pandas_index].to_dict()
                value = row[column]

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
                        f"row {row_number}, "
                        f"column '{column}': {e}"
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

        # --------------------------------
        # AI DATASET SUMMARY
        # --------------------------------

        print("\n--- AI DATASET SUMMARY ---")

        total_rows = len(df)
        total_columns = len(df.columns)

        total_nulls = sum(
            data["missing_values"]
            for data in null_results.values()
        )

        null_columns = {
            column: data["missing_values"]
            for column, data in null_results.items()
            if data["missing_values"] > 0
        }

        total_outliers = sum(
            data["outlier_count"]
            for data in outlier_results.values()
        )

        outlier_columns = {
            column: data["outlier_count"]
            for column, data in outlier_results.items()
            if data["outlier_count"] > 0
        }

        type_issues = {
            column: data
            for column, data in type_results.items()
            if data["status"] != "OK"
        }

        duplicate_count = duplicate_results["exact_duplicates"]

        summary_data = {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "total_nulls": total_nulls,
            "null_columns": null_columns,
            "total_outlier_flags": total_outliers,
            "outlier_columns": outlier_columns,
            "type_issue_count": len(type_issues),
            "type_issues": type_issues,
            "exact_duplicate_count": duplicate_count
        }

        try:

            ai_summary = generate_dataset_summary(
                summary_data
            )

            print("\nAI Dataset Summary:")
            print(ai_summary)

        except Exception as e:

            print(
                f"AI dataset summary failed: {e}"
            )

            ai_summary = None

    # --------------------------------
    # RESULTS
    # --------------------------------

    results = {
        "file": file_path,
        "nulls": null_results,
        "outliers": outlier_results,
        "types": type_results,
        "duplicates": duplicate_results,
        "ai_explanations": ai_explanations,
        "ai_summary": ai_summary
    }

    # --------------------------------
    # SAVE JSON
    # --------------------------------

    output_file = os.path.join(
        output_folder,
        "results.json"
    )

    with open(output_file, "w") as f:

        json.dump(
            results,
            f,
            indent=4
        )

    print(
        f"\nResults saved to: {output_file}"
    )

    # --------------------------------
    # GENERATE HTML REPORT
    # --------------------------------

    print(
        "\n--- GENERATING HTML REPORT ---"
    )

    from generate_report import generate_report

    generate_report(
        file_path,
        output_folder
    )

    print(
        "\n========== FULL PIPELINE COMPLETED ==========\n"
    )
