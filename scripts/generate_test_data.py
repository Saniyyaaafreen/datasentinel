import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_DIR = Path("data")


def generate_clean_data():
    rows = []

    base_time = datetime(2026, 9, 1, 10, 0, 0)

    for i in range(1, 101):
        rows.append({
            "user_id": f"user_{(i % 20) + 1:03d}",
            "event_name": [
                "app_open",
                "level_start",
                "level_complete",
                "purchase",
                "ad_impression"
            ][i % 5],
            "timestamp": base_time + timedelta(minutes=i * 3),
            "session_id": f"session_{(i % 10) + 1:03d}",
            "platform": "iOS" if i % 2 == 0 else "Android",
            "revenue_usd": round(0.99 + (i % 5) * 1.50, 2)
        })

    return pd.DataFrame(rows)


def inject_errors(df):
    dirty = df.copy()

    # 1. Inject a null user_id
    dirty.loc[5, "user_id"] = None

    # 2. Inject a null revenue value
    dirty.loc[20, "revenue_usd"] = None

    # 3. Inject an exact duplicate row
    dirty = pd.concat(
        [dirty, dirty.iloc[[30]]],
        ignore_index=True
    )

    # 4. Inject an impossible future timestamp
    dirty.loc[40, "timestamp"] = "2099-01-01 00:00:00"

    # 5. Inject an impossible timestamp far in the past
    dirty.loc[60, "timestamp"] = "1900-01-01 00:00:00"

    # 6. Inject negative revenue
    dirty.loc[70, "revenue_usd"] = -49.99

    # Convert timestamps to strings for CSV output
    dirty["timestamp"] = dirty["timestamp"].astype(str)

    return dirty


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    clean_df = generate_clean_data()
    dirty_df = inject_errors(clean_df)

    clean_path = OUTPUT_DIR / "sdk_event_logs_clean.csv"
    dirty_path = OUTPUT_DIR / "sdk_event_logs_dirty.csv"

    clean_df.to_csv(clean_path, index=False)
    dirty_df.to_csv(dirty_path, index=False)

    print(f"Clean dataset created: {clean_path}")
    print(f"Dirty dataset created: {dirty_path}")
    print(f"Clean rows: {len(clean_df)}")
    print(f"Dirty rows: {len(dirty_df)}")


if __name__ == "__main__":
    main()
