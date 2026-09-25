from kafka import KafkaProducer
import json
import pandas as pd
import time

# did this before  pip install kafka-python
# localhost:9092 itself doesn't use PLAINTEXT; the Kafka connection to that address is configured as PLAINTEXT.
kafka_url= "kafka:9092" # it use PLAINTEXT as a protocaol already defined in docker compose , dont use https
producer= KafkaProducer(bootstrap_servers=kafka_url)

order1={
    "order_id":1001,
    "customer_id": 10,
    "price":250
}

order2={
    "order_id":1002,
    "customer_id": 20,
    "price":300
}

order3={
    "order_id":1003,
    "customer_id": 30,
    "price":500
}

order4={
    "order_id":1004,
    "customer_id": 40,
    "price":566
}

order5={
    "order_id":1005,
    "customer_id": 50,
    "price":566
}

order6={
    "order_id":1006,
    "customer_id": 60,
    "price":566
}

orders=[order1,
        order2,
        order3,
        order4,
        order5,
        order6]

for order in orders:
    order_json=json.dumps(order)
    order_bytes=order_json.encode("utf-8")
    customer_id=str(order["customer_id"]).encode("utf-8")
    print("customer_id:", order["customer_id"], "key:", customer_id)
    
    future=producer.send(
        "orders",
        key=customer_id,
        value=order_bytes
    )
    metadata=future.get(timeout=5)
    partition=metadata.partition
    offset=metadata.offset
    print("partition:",partition, "offset:", offset)

