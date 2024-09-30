# Build and run containers
docker build -t rss-consumer .
docker run -d --name rss-consumer-container rss-consumer
