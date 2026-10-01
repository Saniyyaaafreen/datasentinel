# DataSentinel SDK Event Log Demo

## Overview

This demo shows how DataSentinel can validate a synthetic mobile game SDK event log and identify common data-quality problems that can occur in analytics and event-tracking pipelines.

The dataset simulates SDK events containing:

* `user_id`
* `event_name`
* `timestamp`
* `session_id`
* `platform`
* `revenue_usd`

The clean dataset contains 100 event records. A dirty version was then generated with intentional data-quality issues.

## Synthetic SDK Dataset

The dataset was generated using:

`scripts/generate_test_data.py`

Two datasets were created:

`data/sdk_event_logs_clean.csv`

`data/sdk_event_logs_dirty.csv`

The dirty dataset contains 101 rows and 6 columns.

## Intentional Data-Quality Issues

The following problems were injected into the dirty dataset:

| Issue                           | Injected |
| ------------------------------- | -------: |
| Missing `user_id`               |        1 |
| Missing `revenue_usd`           |        1 |
| Exact duplicate row             |        1 |
| Negative `revenue_usd`          |        1 |
| Future timestamp                |        1 |
| Impossible historical timestamp |        1 |

The purpose of these injected errors is to simulate realistic problems that can occur in SDK analytics data.

## DataSentinel Validation

The dirty dataset was processed using:

`python datasentinel.py --input data/sdk_event_logs_dirty.csv --schema data/sdk_schema.json --output reports/sdk_demo --ai`

DataSentinel successfully detected:

### Null validation

* `user_id`: 1 missing value
* `revenue_usd`: 1 missing value
* Total null values: 2

### Duplicate validation

* Exact duplicate rows: 1

### Outlier validation

* `revenue_usd`: 1 statistical outlier

### SDK event validation

The custom SDK validation layer detected:

* Negative revenue: 1
* Future timestamp: 1
* Impossible timestamp: 1

### Type validation

No type issues were detected.

## AI Explanation Layer

The AI layer generated 4 explanations for flagged rows:

1. `revenue_usd` statistical outlier
2. Negative `revenue_usd`
3. Future `timestamp`
4. Impossible historical `timestamp`

The AI explanations are generated from the actual validation reason supplied by DataSentinel. This keeps the explanation tied to the rule that detected the issue rather than asking the model to independently guess what might be wrong.

## AI Dataset Summary

The AI-generated summary was:

> The dataset contains 101 rows and 6 columns, with 2 total nulls affecting user_id (1) and revenue_usd (1), along with 1 exact duplicate row. One outlier was flagged in revenue_usd, and SDK event validation identified 1 negative revenue value, 1 future timestamp, and 1 impossible timestamp. No type issues were detected across the dataset.

## Output

The complete DataSentinel results were saved to:

`reports/sdk_demo/results.json`

An HTML data-quality report was also generated:

`reports/sdk_demo/data_quality_report.html`

The JSON results contain the validation results, SDK-specific validation findings, AI explanations, and AI dataset summary.

## Why This Matters for SDK Analytics

Mobile game analytics pipelines depend on event data being accurate enough for downstream analysis, reporting, monetization tracking, and debugging.

Examples of problematic event data include:

* Revenue values that are negative when they should not be
* Events appearing to occur in the future
* Invalid historical timestamps
* Missing identifiers
* Duplicate events
* Statistically unusual values

This demo shows how DataSentinel can combine general-purpose data-quality checks with domain-specific SDK event validation.

## Result

The Day 13 SDK simulation successfully demonstrated:

Synthetic SDK data
↓
Intentional data corruption
↓
DataSentinel validation
↓
SDK-specific validation
↓
AI explanations
↓
AI dataset summary
↓
JSON + HTML report

