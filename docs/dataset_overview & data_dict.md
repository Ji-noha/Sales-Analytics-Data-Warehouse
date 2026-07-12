# 
order_id :Customer placed this order
order_item_id = 1: First product in this order
product_id: The product that was bought
seller_id: The seller of that product
# customers dataset: contains info about the customer(=city, =""cus id"", cust unique_id, customer_zip,=customer_state)

# geolocation : contains ""geo zip code""; = geo state ,= geo city, geo ing, geo lat

# order items: info about orders:  = order id ,="" order item id"", product id, seller id, shipping limit, = price, freight value

# order payments: info about payemnts:  order id, = ""payment sequentiel""; = pay type, pay installments, =pay value

# order reviews: opinions about orders: ""review id"", order id, = review score, = review comment title, rev comm msg, review creation date, rev answer timestamp

# orders: = ""order id"", cussomer id, = order status, = order purchase, order approved at , or delivered carrier date, or del customer date, = order estimated delv date

# products: ""pro id"",= pro category name ,= pro name, pro description, pro photos qty, pro weight , pro length, pro height , pro width

# sellers: ""seller id"", seller zip code; =seller city,= seller state

# pro category name translation:  product category name ,= "" pro categ name english""

Cardinalities
Customers → Orders

One customer can place many orders.

Customers (1) -------- (N) Orders
Orders → Order_Items

One order can contain many products.

Orders (1) -------- (N) Order_Items
Order_Items → Products

Many order items can refer to the same product.

Order_Items (N) -------- (1) Products
Order_Items → Sellers

One seller can sell many order items.

Order_Items (N) -------- (1) Sellers
Orders → Payments

One order can have several payments.

Orders (1) -------- (N) Payments
Orders → Reviews

In Olist, an order has at most one review.

Orders (1) -------- (1) Reviews

(You can use 1→1 for simplicity.)

Products → Category Translation

Many products belong to the same category.

Products (N) -------- (1) Category_Translation

Your simplified ER diagram

                 Customers
                     │
                   1 │ N
                     ▼
                  Orders
          ┌────────┼────────┐
          │        │        │
        1 │      1 │ N    1 │ 1
          ▼        ▼        ▼
      Reviews   Payments  Order_Items
                             │      │
                           N │      │ N
                             ▼      ▼
                        Products   Sellers
                             │
                           N │ 1
                             ▼
                  Category_Translation