import zmq
import atexit
import gzip
from const import BISON, envelopes

channel = envelopes.RIG_KV6


def exit_handler():
    print("Unsubscribing from %s" % channel)
    sock.unsubscribe(channel)


atexit.register(exit_handler)


context = zmq.Context.instance()
sock = context.socket(socket_type=zmq.SUB)
sock.connect(BISON)

sock.subscribe(channel)

for i in range(0, 20):
    if i % 2 == 0:
        print("Receiving from channel %s" % sock.recv())
        continue
    raw_compressed_response = sock.recv()
    raw_response = gzip.decompress(raw_compressed_response)
    print(raw_response)
