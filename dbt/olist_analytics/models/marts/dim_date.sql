WITH dates AS (
    SELECT DISTINCT
        DATE(order_purchase_at) AS date
    FROM {{ ref('int_sales') }}
    )

SELECT 
    date,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(DAYOFWEEK FROM date) AS day_of_week
FROM dates