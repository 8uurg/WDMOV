# Requirements
- Docker
- Python 3
- pipenv
- Java 8
- Maven

# Kafka in Docker Container

Alternatives considered:

- [wurstmeister/kafka-docker](https://github.com/wurstmeister/kafka-docker): runs separate containers for kafka and zookeeper, requires docker-compose
- [spotify/docker-kafka](https://github.com/spotify/docker-kafka): runs zookeeper and kafka in same container, can be run directly with docker

Eventually chose for Spotify's Kafka Docker Image, which requires minimal configuration in this repository.

# Running experiments

First, make sure the GTFS OpenOV NL data are downloaded by running:
```
./download-data.sh
```

Then start the Apache Kafka cluster by running:
```
./cluster/start-cluster.sh
```

Now start the processor, by building the Java project in `/processors` using Maven, and running the main class for the closest stop query (`nl.tudelft.ClosestStop`).

Finally, run the consumer and the producer by executing the corresponding Python scripts in separate terminals. These rely on `pipenv` for dependency management.

Run consumer:
```
cd consumers
pipenv run ./closest_stop_consumer.py
```

Run producer:
```
cd producers
pipenv run ./stops_producer.py
```

After the while, in the consumer terminal you should observe the stop closest to the point hard coded in the processor.

When done, stop and remove the docker container by running:
```
./cluster/stop-cluster.sh
```
