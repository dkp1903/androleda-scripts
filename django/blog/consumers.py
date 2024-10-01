from kafka import KafkaConsumer
import json
import requests

KAFKA_TOPIC = 'rss_feeds'
KAFKA_BROKER = 'localhost:9092'
DJANGO_API_ENDPOINT = 'http://localhost:8000/blogs/ingest/'

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    blog_data = message.value
    try:
        response = requests.post(DJANGO_API_ENDPOINT, json=blog_data)
        response.raise_for_status()
        print(f"Blog '{blog_data['title']}' ingested successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Django API: {e}")
