import sys
import subprocess

if len(sys.argv) != 3:
    print("Usage: python scripts/run_checks.py data.csv schema.json")
    sys.exit()

file_path = sys.argv[1]
schema_path = sys.argv[2]

print("\n========== FULL DATA QUALITY PIPELINE ==========\n")

print("\n--- NULL CHECK ---\n")
subprocess.run(["python", "scripts/check_nulls.py", file_path])

print("\n--- OUTLIER CHECK ---\n")
subprocess.run(["python", "scripts/check_outliers.py", file_path])

print("\n--- TYPE CHECK ---\n")
subprocess.run(["python", "scripts/check_types.py", file_path, schema_path])

print("\n--- DUPLICATE CHECK ---\n")
subprocess.run(["python", "scripts/check_duplicates.py", file_path])

print("\n--- GENERATING HTML REPORT ---\n")
subprocess.run(["python", "scripts/generate_report.py", file_path])

print("\n========== ALL CHECKS COMPLETED ==========")
