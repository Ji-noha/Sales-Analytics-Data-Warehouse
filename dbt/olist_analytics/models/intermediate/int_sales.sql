SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_at,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.shipping_limit_date,
    oi.price,
    oi.freight_value

FROM {{ ref('stg_orders') }} AS o
JOIN {{ ref('stg_order_items') }} AS oi
    ON o.order_id = oi.order_id