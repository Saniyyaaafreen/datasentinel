import pandas as pd


def check_sdk_events(file_path):
    df = pd.read_csv(file_path)

    results = {
        "negative_revenue": {
            "count": 0,
            "indices": []
        },
        "future_timestamps": {
            "count": 0,
            "indices": []
        },
        "impossible_timestamps": {
            "count": 0,
            "indices": []
        }
    }

    # --------------------------------
    # REVENUE VALIDATION
    # --------------------------------

    if "revenue_usd" in df.columns:
        revenue = pd.to_numeric(
            df["revenue_usd"],
            errors="coerce"
        )

        negative_revenue = df[
            revenue < 0
        ]

        results["negative_revenue"] = {
            "count": int(len(negative_revenue)),
            "indices": [
                int(index)
                for index in negative_revenue.index
            ]
        }

    # --------------------------------
    # TIMESTAMP VALIDATION
    # --------------------------------

    if "timestamp" in df.columns:
        timestamps = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        now = pd.Timestamp.now()

        # Future timestamps
        future_timestamps = df[
            timestamps > now
        ]

        results["future_timestamps"] = {
            "count": int(len(future_timestamps)),
            "indices": [
                int(index)
                for index in future_timestamps.index
            ]
        }

        # Timestamps before the year 2000
        impossible_timestamps = df[
            timestamps < pd.Timestamp("2000-01-01")
        ]

        results["impossible_timestamps"] = {
            "count": int(len(impossible_timestamps)),
            "indices": [
                int(index)
                for index in impossible_timestamps.index
            ]
        }

    return results
