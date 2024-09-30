# Example Dockerfile for Node.js Consumer
FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "rss_consumer.js"]
