#!/bin/bash

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start Kafka broker
echo "Starting Kafka broker..."
# Ensure Kafka is running (you may want to include this in a docker-compose)

# Run the producer
echo "Running the RSS producer..."
python rss_producer.py