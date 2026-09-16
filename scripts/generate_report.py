import json
import sys
from datetime import datetime


if len(sys.argv) != 2:
    print("Usage: python scripts/generate_report.py data.csv")
    sys.exit(1)


file_path = sys.argv[1]
results_file = "reports/results.json"
output_file = "reports/data_quality_report.html"


# -------------------------
# Load DataSentinel results
# -------------------------

with open(results_file, "r") as f:
    results = json.load(f)


# -------------------------
# Basic information
# -------------------------

total_rows = 0
total_columns = len(results.get("types", {}))


# -------------------------
# Null results
# -------------------------

null_results = results.get("nulls", {})

total_nulls = sum(
    data.get("missing_values", 0)
    for data in null_results.values()
)


# -------------------------
# Outlier results
# -------------------------

outlier_results = results.get("outliers", {})

total_outlier_flags = sum(
    data.get("outlier_count", 0)
    for data in outlier_results.values()
)


# -------------------------
# Type results
# -------------------------

type_results = results.get("types", {})

type_mismatches = sum(
    1
    for data in type_results.values()
    if data.get("status") != "OK"
)


# -------------------------
# Duplicate results
# -------------------------

duplicate_results = results.get("duplicates", {})

duplicate_count = duplicate_results.get(
    "exact_duplicates",
    0
)


# -------------------------
# AI results
# -------------------------

ai_explanations = results.get(
    "ai_explanations",
    []
)

successful_ai = sum(
    1
    for item in ai_explanations
    if item.get("status") == "SUCCESS"
)


# -------------------------
# Read row count from
# the dataset
# -------------------------

import pandas as pd

df = pd.read_csv(file_path)

total_rows = len(df)
total_columns = len(df.columns)


# -------------------------
# Build HTML
# -------------------------

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>DataSentinel Data Quality Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background-color: #f7f7f7;
    color: #222;
}}

h1 {{
    margin-bottom: 5px;
}}

h2 {{
    margin-top: 35px;
}}

.summary {{
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}}

.card {{
    background: white;
    border: 1px solid #ddd;
    padding: 18px;
    min-width: 150px;
    border-radius: 8px;
}}

.card h3 {{
    margin: 0 0 8px 0;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    background: white;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}

th {{
    background-color: #eeeeee;
}}

.success {{
    color: green;
    font-weight: bold;
}}

.warning {{
    color: #b36b00;
    font-weight: bold;
}}

.ai-box {{
    background: white;
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 12px;
    border-radius: 8px;
}}

.ai-title {{
    font-weight: bold;
    margin-bottom: 6px;
}}

.reason {{
    color: #555;
    margin-bottom: 6px;
}}

</style>

</head>

<body>

<h1>DataSentinel - Data Quality Report</h1>

<p>
<b>File:</b> {file_path}
</p>

<p>
<b>Generated:</b> {datetime.now()}
</p>


<h2>Dataset Summary</h2>

<div class="summary">

<div class="card">
<h3>Total Rows</h3>
<p>{total_rows}</p>
</div>

<div class="card">
<h3>Total Columns</h3>
<p>{total_columns}</p>
</div>

<div class="card">
<h3>Total Nulls</h3>
<p>{total_nulls}</p>
</div>

<div class="card">
<h3>Outlier Flags</h3>
<p>{total_outlier_flags}</p>
</div>

<div class="card">
<h3>Duplicates</h3>
<p>{duplicate_count}</p>
</div>

<div class="card">
<h3>Type Mismatches</h3>
<p>{type_mismatches}</p>
</div>

</div>


<h2>Null Check</h2>

<table>

<tr>
<th>Column</th>
<th>Missing Values</th>
<th>Percentage</th>
<th>Status</th>
</tr>
"""


for column, data in null_results.items():

    missing = data.get("missing_values", 0)
    percentage = data.get("percentage", 0)

    status = (
        '<span class="success">OK</span>'
        if missing == 0
        else '<span class="warning">WARNING</span>'
    )

    html += f"""
<tr>
<td>{column}</td>
<td>{missing}</td>
<td>{percentage}%</td>
<td>{status}</td>
</tr>
"""


html += """

</table>


<h2>Outlier Check</h2>

<table>

<tr>
<th>Column</th>
<th>Outlier Count</th>
<th>Lower Limit</th>
<th>Upper Limit</th>
</tr>
"""


for column, data in outlier_results.items():

    html += f"""
<tr>
<td>{column}</td>
<td>{data.get("outlier_count", 0)}</td>
<td>{data.get("lower_limit", "-")}</td>
<td>{data.get("upper_limit", "-")}</td>
</tr>
"""


html += """

</table>


<h2>Type Check</h2>

<table>

<tr>
<th>Column</th>
<th>Expected Type</th>
<th>Actual Type</th>
<th>Status</th>
</tr>
"""


for column, data in type_results.items():

    status = data.get("status", "UNKNOWN")

    status_html = (
        '<span class="success">OK</span>'
        if status == "OK"
        else '<span class="warning">MISMATCH</span>'
    )

    html += f"""
<tr>
<td>{column}</td>
<td>{data.get("expected", "-")}</td>
<td>{data.get("actual", "-")}</td>
<td>{status_html}</td>
</tr>
"""


html += """

</table>


<h2>Duplicate Check</h2>

<p>
Exact duplicate rows:
<b>
""" + str(duplicate_count) + """
</b>
</p>


<h2>AI Explanations</h2>

<p>
AI explanations generated successfully:
<b>
""" + str(successful_ai) + """
</b>
</p>
"""


# -------------------------
# AI explanation cards
# -------------------------

for item in ai_explanations:

    row_number = item.get("row_number")
    column = item.get("column")
    value = item.get("value")
    reason = item.get("validation_reason")
    explanation = item.get("ai_explanation")

    html += f"""
<div class="ai-box">

<div class="ai-title">
Row {row_number} | Column: {column} | Value: {value}
</div>

<div class="reason">
<b>DataSentinel validation:</b>
{reason}
</div>

<div>
<b>AI explanation:</b>
{explanation}
</div>

</div>
"""


html += """

</body>

</html>
"""


# -------------------------
# Save report
# -------------------------

with open(output_file, "w") as f:
    f.write(html)


print(f"\nReport saved to: {output_file}")

