from kafka import KafkaProducer
import json
import pandas as pd
import time

# did this before  pip install kafka-python
# localhost:9092 itself doesn't use PLAINTEXT; the Kafka connection to that address is configured as PLAINTEXT.

orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")

data=order_items.merge(orders,on="order_id",how="inner")

data=data[
    [ 
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "customer_id",
        "shipping_limit_date",
        "price",
        "freight_value",
        "order_purchase_timestamp"
    ]
]
print(data.head())
print(data.shape)

kafka_url= "kafka:9092" # it use PLAINTEXT as a protocaol already defined in docker compose , dont use https
producer= KafkaProducer(bootstrap_servers=kafka_url,value_serializer=lambda v: json.dumps(v).encode("utf-8"))

for _,row in data.iterrows():
    event=row.to_dict()
    
    future=producer.send(
        "orders",
        value=event
    )
    print("Sent:", event, flush=True)

    time.sleep(0.5)

producer.flush()