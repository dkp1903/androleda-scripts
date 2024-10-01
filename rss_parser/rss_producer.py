# rss_producer.py
import feedparser
from confluent_kafka import Producer
import json

KAFKA_TOPIC = 'rss_feeds'
KAFKA_SERVER = 'localhost:9092'

producer_conf = {'bootstrap.servers': KAFKA_SERVER}
producer = Producer(producer_conf)

def fetch_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        message = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
        }
        # Produce message to Kafka
        producer.produce(KAFKA_TOPIC, json.dumps(message))
        producer.flush()

if __name__ == '__main__':
    rss_feed_url = 'https://github.blog/engineering/feed/'
    fetch_rss_feed(rss_feed_url)
