// rss_consumer.js
const kafka = require('kafka-node');
const mongoose = require('mongoose');

const client = new kafka.KafkaClient({ kafkaHost: 'localhost:9092' });
const consumer = new kafka.Consumer(client, [{ topic: 'rss_feeds', partition: 0 }], { autoCommit: true });

// Connect to MongoDB
mongoose.connect('mongodb://localhost/rss_db', { useNewUrlParser: true, useUnifiedTopology: true });

const rssSchema = new mongoose.Schema({
  title: String,
  link: String,
  published: String,
  summary: String
});

const RSSFeed = mongoose.model('RSSFeed', rssSchema);

consumer.on('message', async function(message) {
  const rssData = JSON.parse(message.value);
  
  const rssFeed = new RSSFeed({
    title: rssData.title,
    link: rssData.link,
    published: rssData.published,
    summary: rssData.summary
  });
  
  // Save to MongoDB
  await rssFeed.save();
  console.log('RSS Feed saved to MongoDB:', rssFeed);
});
