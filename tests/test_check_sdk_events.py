import pandas as pd

from scripts.check_sdk_events import check_sdk_events


def create_csv(tmp_path, rows):
    file_path = tmp_path / "sdk_events.csv"

    df = pd.DataFrame(rows)

    df.to_csv(file_path, index=False)

    return str(file_path)


def test_negative_revenue(tmp_path):
    rows = [
        {
            "user_id": "user_001",
            "event_name": "purchase",
            "timestamp": "2026-09-01 10:00:00",
            "session_id": "session_001",
            "platform": "iOS",
            "revenue_usd": -10.00
        }
    ]

    file_path = create_csv(tmp_path, rows)

    results = check_sdk_events(file_path)

    assert results["negative_revenue"]["count"] == 1


def test_future_timestamp(tmp_path):
    rows = [
        {
            "user_id": "user_001",
            "event_name": "app_open",
            "timestamp": "2099-01-01 00:00:00",
            "session_id": "session_001",
            "platform": "iOS",
            "revenue_usd": 0.0
        }
    ]

    file_path = create_csv(tmp_path, rows)

    results = check_sdk_events(file_path)

    assert results["future_timestamps"]["count"] == 1


def test_impossible_timestamp(tmp_path):
    rows = [
        {
            "user_id": "user_001",
            "event_name": "app_open",
            "timestamp": "1900-01-01 00:00:00",
            "session_id": "session_001",
            "platform": "iOS",
            "revenue_usd": 0.0
        }
    ]

    file_path = create_csv(tmp_path, rows)

    results = check_sdk_events(file_path)

    assert results["impossible_timestamps"]["count"] == 1
