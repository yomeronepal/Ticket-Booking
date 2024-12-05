#!/bin/bash

# Wait for Kafka to be available
echo "Waiting for Kafka to be ready..."
until nc -z -v -w30 kafka 9092
do
  echo "Waiting for Kafka..."
  sleep 5
done

# Once Kafka is available, start the consumer
echo "Kafka is ready. Starting consumer..."
python consumer.py
