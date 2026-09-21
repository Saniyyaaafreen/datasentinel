import argparse
import sys

sys.path.insert(0, "scripts")

from run_checks import run_pipeline


def main():

    parser = argparse.ArgumentParser(
        description="DataSentinel - Automated Data Quality Validation Tool"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input CSV file"
    )

    parser.add_argument(
        "--schema",
        required=True,
        help="Path to the JSON schema file"
    )

    parser.add_argument(
        "--output",
        default="reports/",
        help="Folder where reports will be saved"
    )

    parser.add_argument(
        "--ai",
        action="store_true",
        help="Enable AI-powered explanations and dataset summary"
    )

    args = parser.parse_args()

    print("\n========== DATASENTINEL CLI ==========\n")

    print(f"Input file: {args.input}")
    print(f"Schema file: {args.schema}")
    print(f"Output folder: {args.output}")
    print(f"AI enabled: {args.ai}\n")

    try:

        run_pipeline(
            file_path=args.input,
            schema_path=args.schema,
            output_folder=args.output,
            ai_enabled=args.ai
        )

    except FileNotFoundError as e:

        print(
            f"\nERROR: File not found: {e}"
        )
        sys.exit(1)

    except Exception as e:

        print(
            f"\nERROR: DataSentinel pipeline failed: {e}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
