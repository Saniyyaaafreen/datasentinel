import json
import sys
import pandas as pd

if len(sys.argv) != 3:
    print("Usage: python scripts/check_types.py data.csv schema.json")
    sys.exit()

file_path = sys.argv[1]
schema_path = sys.argv[2]

df = pd.read_csv(file_path)

with open(schema_path, "r") as f:
    schema = json.load(f)

print("\n========== TYPE CHECK ==========\n")

for col, expected in schema.items():

    if col not in df.columns:
        print(f"{col}: MISSING COLUMN")
        continue

    actual = str(df[col].dtype)

    ok = (
        (expected == "int" and "int" in actual) or
        (expected == "float" and ("float" in actual or "int" in actual)) or
        (expected == "string" and "object" in actual)
    )

    if ok:
        print(f"{col}: OK")
    else:
        print(f"{col}: MISMATCH (expected {expected}, got {actual})")
