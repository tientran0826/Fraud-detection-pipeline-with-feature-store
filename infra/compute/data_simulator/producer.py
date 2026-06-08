import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = "user-events"
DATASET_PATH = os.getenv(
    "DATASET_PATH",
    "data/creditcard.csv",
)

df = pd.read_csv(DATASET_PATH)
print("Dataset loaded successfully")
print(f"Dataset shape: {df.shape}")
FEATURE_COLUMNS = [col for col in df.columns if col != "Class"]
current_idx = 0


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
    global current_idx

    row = df.iloc[current_idx]

    current_idx += 1

    if current_idx >= len(df):
        current_idx = 0

    return {column: float(row[column]) for column in FEATURE_COLUMNS}


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
                f"📤 Event {event_count}: "
                f"Time={event['Time']}, "
                f"Amount={event['Amount']} "
                f"→ {KAFKA_TOPIC}"
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
