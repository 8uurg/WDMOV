#!/bin/sh

# https://gist.github.com/abacaphiliac/f0553548f9c577214d16290c2e751071

echo '[1] Pulling dependency Docker image (spotify/kafka)'
docker pull spotify/kafka
docker run -d -p 0.0.0.0:2181:2181 -p 0.0.0.0:9092:9092 --env ADVERTISED_HOST=0.0.0.0 --env ADVERTISED_PORT=9092 --hostname kafka --name kafka spotify/kafka

echo '[2] Waiting 5 seconds for the container to launch the kafka broker'
sleep 5

echo '[3] Creating topics'
docker exec kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic streams-stops-input
docker exec kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic streams-closest-stop-output
