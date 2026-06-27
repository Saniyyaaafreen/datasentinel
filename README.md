# DataSentinel - Day 3

## check_nulls.py

### Description

`check_nulls.py` is a Python script that analyzes a CSV file and generates a report of missing values for every column.

The script calculates:

* Number of missing values
* Percentage of missing values
* Warning for columns with more than 10% missing data

---

## Requirements

* Python 3
* pandas

Install pandas if needed:

```bash
pip install pandas
```

---

## How to Run

From the project root directory:

```bash
python scripts/check_nulls.py data/automobile_cleaned.csv
```

You can also run it with any other CSV file by replacing the filename.

---

## Example Output

```
========== NULL VALUE REPORT ==========

Column: price
Missing Values : 0
Percentage     : 0.00%
----------------------------------------
```

---

## Project Structure

```
datasentinel/
├── data/
├── notebooks/
├── scripts/
│   └── check_nulls.py
└── README.md
```
