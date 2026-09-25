import pandas as pd

from scripts.check_duplicates import check_duplicates


def test_no_duplicates(tmp_path):
    file = tmp_path / "no_duplicates.csv"

    df = pd.DataFrame({
        "name": ["A", "B", "C"],
        "age": [20, 25, 30]
    })

    df.to_csv(file, index=False)

    result = check_duplicates(file)

    assert result["total_rows"] == 3
    assert result["exact_duplicates"] == 0
    assert result["duplicate_indices"] == []
    assert result["near_duplicate_check"] == "skipped"


def test_exact_duplicates(tmp_path):
    file = tmp_path / "exact_duplicates.csv"

    df = pd.DataFrame({
        "name": ["A", "B", "B", "C"],
        "age": [20, 25, 25, 30]
    })

    df.to_csv(file, index=False)

    result = check_duplicates(file)

    assert result["total_rows"] == 4
    assert result["exact_duplicates"] == 1
    assert result["duplicate_indices"] == [2]


def test_near_duplicates(tmp_path):
    file = tmp_path / "near_duplicates.csv"

    df = pd.DataFrame({
        "user_id": [1, 1, 2],
        "timestamp": [
            "2026-09-20 10:00:00",
            "2026-09-20 10:03:00",
            "2026-09-20 11:00:00"
        ]
    })

    df.to_csv(file, index=False)

    result = check_duplicates(file)

    assert result["near_duplicate_count"] == 1
    assert result["near_duplicate_check"] == "performed"


def test_near_duplicates_outside_five_minutes(tmp_path):
    file = tmp_path / "outside_five_minutes.csv"

    df = pd.DataFrame({
        "user_id": [1, 1],
        "timestamp": [
            "2026-09-20 10:00:00",
            "2026-09-20 10:06:00"
        ]
    })

    df.to_csv(file, index=False)

    result = check_duplicates(file)

    assert result["near_duplicate_count"] == 0
    assert result["near_duplicate_check"] == "performed"
