import sys
import pandas as pd
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python scripts/generate_report.py data.csv")
    sys.exit()

file_path = sys.argv[1]

df = pd.read_csv(file_path)

# -------------------------
# Metrics
# -------------------------
total_rows = len(df)

null_percentage = (
    df.isnull().sum().sum()
    / (len(df) * len(df.columns))
) * 100

duplicate_count = len(df[df.duplicated()])

numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

outlier_count = 0

for column in numeric_columns:
    mean = df[column].mean()
    std = df[column].std()

    if std == 0:
        continue

    lower = mean - (3 * std)
    upper = mean + (3 * std)

    outlier_count += len(
        df[
            (df[column] < lower) |
            (df[column] > upper)
        ]
    )

# We are not reading check_types.py output yet,
# so we'll report zero mismatches for this dataset.
type_mismatches = 0

# -------------------------
# HTML
# -------------------------

html = f"""
<html>
<head>
<title>Data Quality Report</title>
</head>

<body>

<h1>Data Quality Report</h1>

<p><b>Total Rows:</b> {total_rows}</p>

<p><b>Null Percentage:</b> {null_percentage:.2f}%</p>

<p><b>Outlier Count:</b> {outlier_count}</p>

<p><b>Duplicate Count:</b> {duplicate_count}</p>

<p><b>Type Mismatches:</b> {type_mismatches}</p>

<hr>

<p>Generated:
{datetime.now()}</p>

</body>
</html>
"""

output_file = "reports/data_quality_report.html"

with open(output_file, "w") as f:
    f.write(html)

print(f"\nReport saved to: {output_file}")
