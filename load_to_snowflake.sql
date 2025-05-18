-- Step 1: Create a staging table
CREATE OR REPLACE TABLE churn_predictions_raw (
    customer_id STRING,
    gender STRING,
    age INTEGER,
    tenure INTEGER,
    monthly_charge FLOAT,
    total_charge FLOAT,
    support_calls INTEGER,
    churn INTEGER,
    churn_prediction INTEGER
);

-- Step 2: Create or use a file format (CSV)
CREATE OR REPLACE FILE FORMAT csv_format
TYPE = 'CSV'
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
SKIP_HEADER = 1;

-- Step 3: Create a named stage (optional if using PUT directly)
CREATE OR REPLACE STAGE churn_stage
FILE_FORMAT = csv_format;

-- Step 4: Upload the file from your local machine using SnowSQL
-- Terminal command (run outside SQL): 
-- snowsql -a <account> -u <user> -f load_to_snowflake.sql
-- PUT file://<path>/churn_predictions.csv @churn_stage AUTO_COMPRESS=TRUE;

-- Step 5: Load the data
COPY INTO churn_predictions_raw
FROM @churn_stage
FILE_FORMAT = (FORMAT_NAME = 'csv_format');
