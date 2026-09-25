import pandas as pd

from scripts.check_nulls import check_nulls


def test_no_nulls(tmp_path):
    file = tmp_path / "no_nulls.csv"

    df = pd.DataFrame({
        "name": ["A", "B", "C"],
        "age": [20, 25, 30]
    })

    df.to_csv(file, index=False)

    result = check_nulls(file)

    assert result["name"]["missing_values"] == 0
    assert result["age"]["missing_values"] == 0


def test_all_nulls(tmp_path):
    file = tmp_path / "all_nulls.csv"

    df = pd.DataFrame({
        "name": [None, None, None]
    })

    df.to_csv(file, index=False)

    result = check_nulls(file)

    assert result["name"]["missing_values"] == 3
    assert result["name"]["percentage"] == 100.0
    assert result["name"]["warning"] is True


def test_partial_nulls(tmp_path):
    file = tmp_path / "partial_nulls.csv"

    df = pd.DataFrame({
        "name": ["A", None, "C", None]
    })

    df.to_csv(file, index=False)

    result = check_nulls(file)

    assert result["name"]["missing_values"] == 2
    assert result["name"]["percentage"] == 50.0
    assert result["name"]["warning"] is True


def test_empty_dataframe(tmp_path):
    file = tmp_path / "empty.csv"

    df = pd.DataFrame({
        "name": [],
        "age": []
    })

    df.to_csv(file, index=False)

    result = check_nulls(file)

    assert result["name"]["missing_values"] == 0
    assert result["name"]["percentage"] == 0
    assert result["name"]["warning"] is False

    assert result["age"]["missing_values"] == 0
    assert result["age"]["percentage"] == 0
    assert result["age"]["warning"] is False
