import sys
import pandas as pd

# Check if the user provided a CSV file
if len(sys.argv) != 2:
    print("Usage: python scripts/check_nulls.py data/yourfile.csv")
    sys.exit(1)

# Get the file path from the command line
file_path = sys.argv[1]

try:
    # Read the CSV file
    df = pd.read_csv(file_path)

    print("\n========== NULL VALUE REPORT ==========\n")

    total_rows = len(df)

    for column in df.columns:
        null_count = df[column].isnull().sum()
        percentage = (null_count / total_rows) * 100

        print(f"Column: {column}")
        print(f"Missing Values : {null_count}")
        print(f"Percentage     : {percentage:.2f}%")

        if percentage > 10:
            print("⚠ WARNING: More than 10% missing values!")

        print("-" * 40)

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")

except Exception as e:
    print(f"An error occurred: {e}")