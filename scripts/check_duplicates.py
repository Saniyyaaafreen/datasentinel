import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python scripts/check_duplicates.py data.csv")
    sys.exit()

file_path = sys.argv[1]

df = pd.read_csv(file_path)

print("\n========== DUPLICATE REPORT ==========\n")

# Exact duplicates
exact_duplicates = df[df.duplicated()]

print(f"Total rows: {len(df)}")
print(f"Exact duplicate rows: {len(exact_duplicates)}")

# Near duplicates (only if user_id and timestamp exist)
if "user_id" in df.columns and "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values(["user_id", "timestamp"])

    df["time_diff"] = (
        df.groupby("user_id")["timestamp"]
          .diff()
          .dt.total_seconds()
    )

    near_duplicates = df[
        (df["time_diff"] > 0) &
        (df["time_diff"] <= 300)
    ]

    print(f"Near duplicates (within 5 minutes): {len(near_duplicates)}")
else:
    print("Near duplicate check skipped (user_id/timestamp not found).")
