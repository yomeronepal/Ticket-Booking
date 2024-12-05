from kafka import KafkaConsumer, errors
import json
import os
import time
import logging

# Set up logging to stdout
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

# Example logging
logger.info("Kafka consumer started")


def consume_messages(topics):
    """
    Consumes messages from the given Kafka topics.
    Args:
        topics (list): A list of Kafka topic names to subscribe to.
    """
    kafka_host = os.getenv("KAFKA_HOST", "kafka:9092")

    # Retry mechanism
    retries = 20
    for attempt in range(retries):
        try:
            logger.info(
                f"Attempt {attempt + 1}: Connecting to Kafka at {kafka_host}..."
            )
            consumer = KafkaConsumer(
                *topics,  # Unpacking the list of topics
                bootstrap_servers=kafka_host,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="flask-group",
            )
            logger.info("Connected to Kafka successfully.")
            break  # Exit the retry loop if successful
        except errors.NoBrokersAvailable:
            logger.info("Kafka broker is not available. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
    else:
        logger.info(f"Failed to connect to Kafka after {retries} attempts.")

    # Start consuming messages
    for message in consumer:
        logger.info(f"Consumed message from topic '{message.topic}': {message.value}")


if __name__ == "__main__":
    topics = ["flask_topic", "ticket_availability", "payment_notifications", "waitlist"]
    consume_messages(topics)
