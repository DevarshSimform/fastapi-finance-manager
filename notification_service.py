import json
import os

from kafka import KafkaConsumer

from src.utils.email_util import send_verification_email

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

consumer = KafkaConsumer(
    "2fa_verification_requested",
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset="earliest",
    group_id="notification-service",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("Notification Service is listening...")

for message in consumer:
    payload = message.value
    try:
        send_verification_email(payload["to_email"], payload["data"])
        print(f"Sent email to {payload['to_email']} - FROM Kafka consumer")
    except Exception as e:
        print(f"Failed to queue email task for {payload['to_email']}: {e}")
        consumer.close()
