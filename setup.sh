# Install Kafka and Zookeeper
sudo apt-get install kafka
sudo apt-get install zookeeper

# Start Zookeeper
zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
kafka-server-start.sh config/server.properties

# Create Kafka topic
kafka-topics.sh --create --topic rss_feeds --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
