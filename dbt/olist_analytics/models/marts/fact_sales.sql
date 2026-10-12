{{ config(
    materialized='table',
    unique_key=['order_id','order_item_id'],
    partition_by = {
        "field": "order_date",
        "data_type": "date"
    },
    cluster_by = ["customer_id", "product_id"]
) }}

SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    customer_id,
    price,
    freight_value,
    order_purchase_at,
    DATE(order_purchase_at) AS order_date

FROM {{ ref('int_sales') }}

{% if is_incremental() %}
    WHERE order_purchase_at > (
        SELECT MAX(order_purchase_at)
        FROM {{this}} 
    )

{% endif %}

