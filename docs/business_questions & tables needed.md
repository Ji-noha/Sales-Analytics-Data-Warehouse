## Section 1 — Revenue Analysis: CEO
* total revenue? order_items[price] 

* monthly revenue? orders[order_purchase_timestamp] -> order_items[price]

* month had the highest revenue?
orders[order_purchase_timesatmp] & orders[order_id]->order_items[price]

* state generates the most revenue? customers[customer_state] ->orders[customer_id]+orders[order_id] -> order_items[price]


* the average order value:
orders[order_id] -> order_items[price]

* How much revenue does each seller generate? order_items[seller_id] & order_items[price]

## Section 2 — Customer Analysis: marketing team
* How many customers do we have? customers[cus_unique_id]

* Which cities have the most customers?
customers[customer_city] & customers[cus_unique_id]

* Which states have the most customers?
customers[customer_state] & customers[cus_unique_id]

* Who are our top customers?
customers[customer_id]  orders[customer_id]  orders[order_id]  order_items[price]

* How many orders does each customer place?
orders[customer_id] & orders[order_id]
# Section 3 — Product Analysis: product manager

* Which products sell the most?
order_item[product_id]  order_items[order_item_id]

* Which product categories generate the most revenue?
products[category_name] & products[product_id]
& order_item[product_id]
& order_items[price]

* Which categories are least popular?
products[category_name] & products[product_id]
& order_item[product_id]

* Which products have never been sold?
products[product_id]
 order_items[product_id]


* What is the average price by category?
order_item[price] & order_item[product_id] & product[category_name]

# Section 4 — Seller Analysis: management
* How many sellers are there?
seller[seller_id]

* Which sellers generate the most revenue?
order_item[seller_id] & order_item[price]

* Which seller has the most orders?
order_item[seller_id] & order_item[order_id]

* Which states have the most sellers?
sellers[seller_id] & sellers
[seller_state]

# Section 5 — Delivery Analysis: logistics
* What is the average delivery time?
orders[order_deliveredcustomer_date] - orders[order_purchase_timestamp]

* Which states have the longest delivery times?
customers[customer_state]
orders[customer_id] & orders[order_purchase_timestamp] & orders[order_delivered_customer_date]

* How many orders are delivered late?
 orders[order_estimated_delivery_date] & orders[order_delivered_customer_date]

* Which sellers have the fastest deliveries?
order_items[seller_id] &order_items[order_id] & orders[order_delivered_customer_date] & orders[order_purchase_timesatmp]

# Section 6 — Payment Analysis: finance:
* Which payment method is used the most?
order_payemnts[payment_type]

* What is the average payment amount?
order_payemnts[payment_value]

* How many installments do customers usually choose?
order_payemnts[payment_installements]

# Section 7 — Reviews : customer support:
* What is the average review score?
order_reviews[reveiw_score]

* Which products receive the lowest ratings?
order_reviews[reveiw_score] & order_reviews[order_id] &
order_items[order_id] order_items[product_id] & products[product_id]
* Which sellers receive the best ratings?
order_reviews[reveiw_score] & order_reviews[order_id] & order_items[seller_id] & order_items[order_id]