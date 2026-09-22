-- ============================================================
-- DataSentinel - Advanced SQL Data Quality Validation
-- ============================================================
-- Purpose:
-- These SQL queries demonstrate how common DataSentinel
-- validation checks can also be performed directly in SQL.
--
-- Assumption:
-- The cleaned automobile dataset is available as:
-- automobile_cleaned
--
-- The queries use standard SQL concepts where possible.
-- ============================================================


-- ============================================================
-- QUERY 1: NULL VALUE DETECTION
-- DataSentinel equivalent: check_nulls.py
-- ============================================================
-- Find rows where important fields contain NULL values.

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS null_price,
    SUM(CASE WHEN horsepower IS NULL THEN 1 ELSE 0 END) AS null_horsepower,
    SUM(CASE WHEN engine_size IS NULL THEN 1 ELSE 0 END) AS null_engine_size,
    SUM(CASE WHEN city_mpg IS NULL THEN 1 ELSE 0 END) AS null_city_mpg,
    SUM(CASE WHEN highway_mpg IS NULL THEN 1 ELSE 0 END) AS null_highway_mpg
FROM automobile_cleaned;


-- ============================================================
-- QUERY 2: DUPLICATE DETECTION
-- DataSentinel equivalent: check_duplicates.py
-- ============================================================
-- Group by all relevant columns and identify exact duplicate rows.

SELECT
    symboling,
    normalized_losses,
    wheel_base,
    length,
    width,
    height,
    curb_weight,
    engine_size,
    bore,
    stroke,
    compression_ratio,
    horsepower,
    peak_rpm,
    city_mpg,
    highway_mpg,
    price,
    COUNT(*) AS duplicate_count
FROM automobile_cleaned
GROUP BY
    symboling,
    normalized_losses,
    wheel_base,
    length,
    width,
    height,
    curb_weight,
    engine_size,
    bore,
    stroke,
    compression_ratio,
    horsepower,
    peak_rpm,
    city_mpg,
    highway_mpg,
    price
HAVING COUNT(*) > 1;


-- ============================================================
-- QUERY 3: OUTLIER DETECTION
-- DataSentinel equivalent: check_outliers.py
-- ============================================================
-- Identify unusually high/low prices using the 3-standard-
-- deviation rule used by DataSentinel.
--
-- Rows outside:
-- mean - 3*standard_deviation
-- mean + 3*standard_deviation
-- are flagged as potential outliers.

WITH PriceStats AS (
    SELECT
        AVG(price) AS mean_price,
        STDDEV(price) AS std_price
    FROM automobile_cleaned
)
SELECT
    a.price,
    s.mean_price,
    s.std_price,
    CASE
        WHEN a.price < s.mean_price - (3 * s.std_price)
          OR a.price > s.mean_price + (3 * s.std_price)
        THEN 'OUTLIER'
        ELSE 'NORMAL'
    END AS validation_status
FROM automobile_cleaned a
CROSS JOIN PriceStats s
ORDER BY a.price DESC;


-- ============================================================
-- QUERY 4: DATA TYPE / VALUE VALIDATION
-- DataSentinel equivalent: check_types.py
-- ============================================================
-- SQL databases enforce column types through table definitions.
-- This query demonstrates an additional validation layer by
-- checking whether numeric fields contain values outside
-- reasonable business/data ranges.

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN horsepower < 0 THEN 1 ELSE 0 END)
        AS invalid_horsepower,
    SUM(CASE WHEN engine_size <= 0 THEN 1 ELSE 0 END)
        AS invalid_engine_size,
    SUM(CASE WHEN city_mpg <= 0 THEN 1 ELSE 0 END)
        AS invalid_city_mpg,
    SUM(CASE WHEN highway_mpg <= 0 THEN 1 ELSE 0 END)
        AS invalid_highway_mpg,
    SUM(CASE WHEN price <= 0 THEN 1 ELSE 0 END)
        AS invalid_price
FROM automobile_cleaned;


-- ============================================================
-- QUERY 5: DATA QUALITY SUMMARY
-- DataSentinel equivalent: combined validation summary
-- ============================================================
-- Produce a compact SQL-based data quality summary.

SELECT
    COUNT(*) AS total_rows,

    SUM(
        CASE
            WHEN price IS NULL
              OR horsepower IS NULL
              OR engine_size IS NULL
              OR city_mpg IS NULL
              OR highway_mpg IS NULL
            THEN 1
            ELSE 0
        END
    ) AS rows_with_nulls,

    SUM(
        CASE
            WHEN price <= 0
              OR horsepower < 0
              OR engine_size <= 0
              OR city_mpg <= 0
              OR highway_mpg <= 0
            THEN 1
            ELSE 0
        END
    ) AS rows_with_invalid_values,

    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price,
    AVG(price) AS average_price

FROM automobile_cleaned;


-- ============================================================
-- END OF DATASENTINEL SQL VALIDATION
-- ============================================================

