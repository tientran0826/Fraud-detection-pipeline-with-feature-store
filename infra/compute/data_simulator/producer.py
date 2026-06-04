import json
import os
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = "user-events"


def create_producer():
    """Create Kafka producer with exponential backoff retry"""
    retries = 0
    max_retries = 30

    while retries < max_retries:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                request_timeout_ms=10000,
            )
            print(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
            return producer
        except Exception:
            retries += 1
            wait_time = min(2**retries, 30)
            print(f"Kafka not ready, retrying in {wait_time}s... (attempt {retries}/{max_retries})")
            time.sleep(wait_time)

    raise Exception("Failed to connect to Kafka after multiple retries")


def generate_event():
    """Generate simulated user event data"""
    user_id = random.randint(1, 1000)
    # Simulate varying click patterns (including anomalies)
    base_clicks = random.randint(5, 30)
    if random.random() < 0.05:  # 5% chance of anomaly
        click_count = random.randint(150, 300)
    else:
        click_count = base_clicks

    return {
        "user_id": user_id,
        "click_count": click_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": f"session_{user_id}_{int(time.time())}",
    }


def run_producer():
    """Continuously produce events to Kafka"""
    producer = create_producer()

    event_count = 0
    try:
        print(f"Starting data simulator, publishing to topic '{KAFKA_TOPIC}'...")

        while True:
            event = generate_event()

            # Send to Kafka
            future = producer.send(KAFKA_TOPIC, value=event)
            record_metadata = future.get(timeout=10)

            event_count += 1
            print(
                f"📤 Event {event_count}: user_id={event['user_id']}, "
                f"clicks={event['click_count']} → {KAFKA_TOPIC}"
            )

            # Wait 2 seconds before next event
            time.sleep(2)

    except KeyboardInterrupt:
        print(f"Stopping producer after {event_count} events")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        producer.flush()
        producer.close()
        print("Connection closed")


if __name__ == "__main__":
    run_producer()
