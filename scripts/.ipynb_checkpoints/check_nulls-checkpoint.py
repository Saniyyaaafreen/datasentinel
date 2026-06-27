import sys
import pandas as pd

# Check if a file path was provided
if len(sys.argv) != 2:
    print("Usage: python check_nulls.py data/AUTOMOBILE DATASET.csv")
    sys.exit()

file_path = sys.argv[1]

# Load the CSV file
df = pd.read_csv(AUTOMOBILE DATASET.csv)

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