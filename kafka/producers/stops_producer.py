#!/usr/bin/env python3

import sys

from kafka import KafkaProducer
from kafka.errors import KafkaError

import csv
import json

topic = 'streams-stops-input'
stops_file_path = '../data/stops.txt'

producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    api_version=(0,10),
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

def on_send_success(record_metadata):
    print('produced message on {} in partition {} with offset {}'.format(record_metadata.topic, record_metadata.partition, record_metadata.offset))

def on_send_error(e):
    print(e)

with open(stops_file_path, 'r') as stops_file:
    stops_reader = csv.reader(stops_file, delimiter=',', quotechar='"')
    first = True
    count = 0
    for row in stops_reader:
        if (first):
            first = False
            continue

        stop = {
            'id': row[0],
            'name': row[2],
            'latitude': row[3],
            'longitude': row[4]
        }

        # produce message for stop
        producer.send(topic, key=b'1', value=stop).add_callback(on_send_success).add_errback(on_send_error)

        count += 1
        #if (count >= 30): break

# block until all async messages are sent
producer.flush()
