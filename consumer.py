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
    group_id="debug_consumer",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("connected to kafka", flush=True)

for msg in consumer:
    print("message received:", flush=True)
    print(msg.value, flush=True)
    print("partition:", msg.partition, flush=True)
    print("offset:", msg.offset, flush=True)


#cursor.execute("SELECT 1")
#result = cursor.fetchone()
# print(result)
    print("INSERTING INTO POSTGRES", flush=True)

    cursor.execute(
        """
        INSERT INTO staging_orders (order_id, customer_id, price)
        VALUES (%s, %s, %s)
        """,
        (msg.value["order_id"],msg.value["customer_id"],msg.value["price"])
    )

    print("INSERT COMMITTED", flush=True)
    connection.commit()

"""from kafka import KafkaConsumer 
import json
import psycopg2

consumer=KafkaConsumer(
    "orders",
    bootstrap_servers="kafka:9092",
    group_id="new_docker",
    auto_offset_reset="earliest"
)

for msg in consumer:
    message=json.loads(msg.value.decode("utf-8"))
    print(message)
    print("Consumer 1")
    print(msg.partition)
    print(msg.offset)

#connection=f"postgresql+psycopg2://postgres:password@postgres:5432/ecommerce"
"""