# DataSentinel

A Python-based Data Quality Validation Toolkit that performs automated data quality checks on CSV datasets.

## Features

- Detects missing values
- Detects statistical outliers using the 3 Standard Deviation method
- Validates column data types using a JSON schema
- Detects duplicate records
- Generates an HTML Data Quality Report
- Runs all quality checks using a single pipeline script

---

## Project Structure

```
datasentinel/
│
├── data/
│   ├── automobile_cleaned.csv
│   └── schema.json
│
├── scripts/
│   ├── check_nulls.py
│   ├── check_outliers.py
│   ├── check_types.py
│   ├── check_duplicates.py
│   ├── generate_report.py
│   └── run_checks.py
│
├── reports/
│   └── data_quality_report.html
│
├── notebooks/
│
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/Saniyyaaafreen/datasentinel.git
```

Move into the project.

```bash
cd datasentinel
```

Install dependencies.

```bash
pip install pandas
```

---

## Usage

Run the complete data quality pipeline.

```bash
python scripts/run_checks.py data/automobile_cleaned.csv data/schema.json
```

---

## Checks Performed

- Null Value Detection
- Outlier Detection
- Type Validation
- Duplicate Detection
- HTML Report Generation

---

## Sample Output

After execution, an HTML report is generated inside:

```
reports/data_quality_report.html
```

Open it using:

```bash
open reports/data_quality_report.html
```

---

## Technologies Used

- Python
- Pandas
- Git
- GitHub
- JSON
- HTML

---

## Future Improvements

- Email report generation
- Interactive dashboard
- Automatic anomaly detection
- Support for Excel and SQL databases

---

## Author

**Saniyya Aafreen G P**
