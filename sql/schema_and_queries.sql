CREATE DATABASE IF NOT EXISTS job_market;
USE job_market;

CREATE TABLE IF NOT EXISTS job_postings (
  job_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(1000) NOT NULL,
  job_url VARCHAR(1500),
  published_date DATETIME,
  is_hourly BOOLEAN,
  hourly_low DECIMAL(10,2),
  hourly_high DECIMAL(10,2),
  fixed_budget DECIMAL(14,2),
  country VARCHAR(150),
  category VARCHAR(100),
  month_key CHAR(7),
  remote_keyword BOOLEAN,
  INDEX idx_published_date (published_date),
  INDEX idx_country (country),
  INDEX idx_category (category)
);

-- Run after importing jobs_cleaned.csv into job_postings (adjust table/column names if using an import wizard).
-- Task 1: average/median rates by keyword should be calculated from title keyword matches.
SELECT country, COUNT(*) AS hourly_jobs,
       AVG((hourly_low + hourly_high)/2) AS avg_hourly_midpoint
FROM job_postings
WHERE is_hourly = TRUE AND hourly_low IS NOT NULL AND hourly_high IS NOT NULL
GROUP BY country HAVING COUNT(*) >= 30
ORDER BY hourly_jobs DESC;

-- Task 2/6: monthly posting trend
SELECT month_key, COUNT(*) AS postings
FROM job_postings
GROUP BY month_key ORDER BY month_key;

-- Category frequency
SELECT category, COUNT(*) AS postings
FROM job_postings
GROUP BY category ORDER BY postings DESC;

-- Important: hourly rates may not include a currency code; do not compare as if currencies are verified.
