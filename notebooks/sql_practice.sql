-- ===========================================
-- Query 1
-- Count the number of cars for each manufacturer
-- ===========================================

SELECT
    make,
    COUNT(*) AS total_cars
FROM automobile_cleaned
GROUP BY make
ORDER BY total_cars DESC;

-- ===========================================
-- Query 2
-- Show manufacturers with more than 10 cars
-- ===========================================

SELECT
    make,
    COUNT(*) AS total_cars
FROM automobile_cleaned
GROUP BY make
HAVING COUNT(*) > 10
ORDER BY total_cars DESC;

-- ===========================================
-- Query 3
-- CTE to find expensive cars
-- ===========================================

WITH ExpensiveCars AS (
    SELECT
        make,
        price
    FROM automobile_cleaned
    WHERE price > 20000
)

SELECT *
FROM ExpensiveCars
ORDER BY price DESC;

-- ===========================================
-- Query 4
-- Rank cars by price within each manufacturer
-- ===========================================

SELECT
    make,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY make
        ORDER BY price DESC
    ) AS row_num
FROM automobile_cleaned;

-- ===========================================
-- Query 5
-- Compare each car's price with the previous one
-- ===========================================

SELECT
    make,
    price,
    LAG(price) OVER (
        ORDER BY price
    ) AS previous_price
FROM automobile_cleaned;
