#!/usr/bin/env python3

from kafka import KafkaConsumer

topic = 'streams-closest-stop-output'

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(topic,
                         group_id='kafka',
                         bootstrap_servers=['localhost:9092'])

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
