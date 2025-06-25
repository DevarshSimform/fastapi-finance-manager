import json
import os
import signal
import sys
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from src.utils.email_util import send_verification_email

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


def create_consumer(retries=5, delay=5):
    for i in range(retries):
        try:
            consumer = KafkaConsumer(
                "2fa_verification_requested",
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset="earliest",
                group_id="notification-service",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            print("Kafka consumer connected")
            return consumer
        except NoBrokersAvailable:
            print(
                f"Kafka broker not available, retrying in {delay}s... ({i + 1}/{retries})"
            )
            time.sleep(delay)
    raise Exception("Failed to connect to Kafka broker")


consumer = create_consumer()


def shutdown_handler(signal_received, frame):
    print("Shutting down consumer...")
    consumer.close()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

print("Notification Service is listening...")

for message in consumer:
    payload = message.value
    try:
        send_verification_email(payload["to_email"], payload["data"])
        print(f"Sent email to {payload['to_email']} - FROM Kafka consumer")
    except Exception as e:
        print(f"Failed to queue email task for {payload['to_email']}: {e}")
