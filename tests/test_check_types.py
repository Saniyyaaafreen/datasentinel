import json

import pandas as pd

from scripts.check_types import check_types


def create_schema(file, schema):
    with open(file, "w") as f:
        json.dump(schema, f)


def test_matching_types(tmp_path):
    csv_file = tmp_path / "matching.csv"
    schema_file = tmp_path / "schema.json"

    df = pd.DataFrame({
        "age": [20, 25, 30],
        "price": [100.5, 200.0, 300.5],
        "name": ["A", "B", "C"]
    })

    df.to_csv(csv_file, index=False)

    schema = {
        "age": "int",
        "price": "float",
        "name": "string"
    }

    create_schema(schema_file, schema)

    result = check_types(csv_file, schema_file)

    assert result["age"]["status"] == "OK"
    assert result["price"]["status"] == "OK"
    assert result["name"]["status"] == "OK"


def test_type_mismatch(tmp_path):
    csv_file = tmp_path / "mismatch.csv"
    schema_file = tmp_path / "schema.json"

    df = pd.DataFrame({
        "age": ["twenty", "twenty-five", "thirty"]
    })

    df.to_csv(csv_file, index=False)

    schema = {
        "age": "int"
    }

    create_schema(schema_file, schema)

    result = check_types(csv_file, schema_file)

    assert result["age"]["status"] == "MISMATCH"
    assert result["age"]["expected"] == "int"


def test_missing_column(tmp_path):
    csv_file = tmp_path / "missing_column.csv"
    schema_file = tmp_path / "schema.json"

    df = pd.DataFrame({
        "age": [20, 25, 30]
    })

    df.to_csv(csv_file, index=False)

    schema = {
        "age": "int",
        "name": "string"
    }

    create_schema(schema_file, schema)

    result = check_types(csv_file, schema_file)

    assert result["age"]["status"] == "OK"
    assert result["name"]["status"] == "MISSING COLUMN"
    assert result["name"]["actual"] is None


def test_integer_allowed_for_float(tmp_path):
    csv_file = tmp_path / "integer_as_float.csv"
    schema_file = tmp_path / "schema.json"

    df = pd.DataFrame({
        "price": [100, 200, 300]
    })

    df.to_csv(csv_file, index=False)

    schema = {
        "price": "float"
    }

    create_schema(schema_file, schema)

    result = check_types(csv_file, schema_file)

    assert result["price"]["status"] == "OK"
