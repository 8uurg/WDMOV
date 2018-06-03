# Initial version from streaming-data/data_processor.py
# Together with streaming-data/merger.py

import zmq
import gzip
import atexit
from const import Envelopes, BISON
from bs4 import BeautifulSoup
import psycopg2

channels = [
    Envelopes.KV6_ARR,
    #Envelopes.KV6_CXX,
    #Envelopes.KV6_DITP,
    #Envelopes.KV6_EBS,
    #Envelopes.KV6_GVB,
    #Envelopes.KV6_RIG,
    #Envelopes.KV6_QBUZZ,
]

conn = psycopg2.connect(user="postgres", host="db")
cur = conn.cursor()

context = zmq.Context.instance()
sock = context.socket(socket_type=zmq.SUB)
sock.connect(BISON)
print("Connected")

for ch in channels:
    sock.subscribe(ch)

def exit_handler():
    for ch in channels:
        print("Unsubscribing from %s" % ch)
        sock.unsubscribe(ch)
    context.destroy()
    conn.close()


atexit.register(exit_handler)

while True:
    topic = sock.recv() # Envelope
    raw_data = sock.recv()
    data = gzip.decompress(raw_data)
    print("Recieved message on {}".format(topic))
    # print(data)
    soup = BeautifulSoup(data, features="xml")
    posinfo = soup('VV_TM_PUSH')('KV6posinfo')
    # TODO: extract this info.
