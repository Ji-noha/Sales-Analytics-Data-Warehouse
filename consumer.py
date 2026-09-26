from kafka import KafkaConsumer
import json
import psycopg2

connection = psycopg2.connect(
    host="postgres",
    port=5432,
    database="ecommerce",
    user="postgres",
    password="password"
)
cursor = connection.cursor()

print("Consumer1", flush=True)

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="kafka:9092",
    group_id="streaming_orders_v1",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("connected to kafka", flush=True)

for msg in consumer:
    print("message received:", flush=True)
    print(msg.value, flush=True)
    print("partition:", msg.partition, flush=True)
    print("offset:", msg.offset, flush=True)

    cursor.execute(
        """
        INSERT INTO staging_orders (
            order_id,
            order_item_id,
            product_id,
            seller_id,
            customer_id,
            shipping_limit_date,
            price,
            freight_value,
            order_purchase_timestamp
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            msg.value["order_id"],
            msg.value["order_item_id"],
            msg.value["product_id"],
            msg.value["seller_id"],
            msg.value["customer_id"],
            msg.value["shipping_limit_date"],
            msg.value["price"],
            msg.value["freight_value"],
            msg.value["order_purchase_timestamp"]
        )
    )

    connection.commit()

