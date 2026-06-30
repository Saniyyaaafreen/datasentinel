import sys
import pandas as pd

# -----------------------------
# STEP 1: Get file from terminal
# -----------------------------
if len(sys.argv) != 2:
    print("Usage: python scripts/check_outliers.py data/file.csv")
    sys.exit()

file_path = sys.argv[1]

# -----------------------------
# STEP 2: Load dataset
# -----------------------------
df = pd.read_csv(file_path)

print("\n========== OUTLIER REPORT ==========\n")

# -----------------------------
# STEP 3: Select numeric columns
# -----------------------------
numeric_columns = df.select_dtypes(include="number").columns

# -----------------------------
# STEP 4: Loop through columns
# -----------------------------
for column in numeric_columns:

    mean = df[column].mean()
    std = df[column].std()

    lower_limit = mean - (3 * std)
    upper_limit = mean + (3 * std)

    outliers = df[
        (df[column] < lower_limit) |
        (df[column] > upper_limit)
    ]

    print("Column:", column)
    print("Mean:", round(mean, 2))
    print("Std Dev:", round(std, 2))
    print("Outliers:", len(outliers))
    print("-" * 40)
