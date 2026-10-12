SELECT 
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp AS order_purchase_at

FROM {{ source('olist_raw', 'raw_orders') }}