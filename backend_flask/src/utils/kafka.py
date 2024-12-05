from kafka import KafkaProducer
import os
import json


class KafkaProducerClient:
    def __init__(self):
        # Kafka configuration
        kafka_config = {
            "bootstrap_servers": os.environ.get("KAFKA_HOST"),
            "client_id": "flask-producer",
            "api_version": (2, 5, 0),  # Set API version to match your Kafka broker
            "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
        }

        # Initialize Kafka Producer
        self.client = KafkaProducer(**kafka_config)


class KafkaPublisher(KafkaProducerClient):
    def send(self, topic, message):
        self.client.send(topic, message)
        self.client.flush()
