from kafka import KafkaConsumer
import json

consumer2=KafkaConsumer(
    "orders",
    bootstrap_servers="kafka:9092",
    group_id="test_orders_2",
    auto_offset_reset="earliest"
    )


for msg in consumer2:
    message=json.loads(msg.value.decode("utf-8"))
    print(message)
    print("Consumer 2")
    print(msg.partition)
    print(msg.offset)