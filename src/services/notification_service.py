import json

from kafka import KafkaConsumer

from src.utils.email_util import send_verification_email_task

consumer = KafkaConsumer(
    "2fa_verification_requested",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="notification-service",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print("Notification Service is listening...")

for message in consumer:
    data = message.value
    try:
        send_verification_email_task.delay(data["to_email"], data)
        print(f"Sent email to {data['to_email']} - FROM Kafka consumer")
    except Exception as e:
        print(f"Failed to queue email task for {data['to_email']}: {e}")
