import zmq
import atexit

from const import BISON, Envelopes

channels = [
    Envelopes.KV6_ARR,
    Envelopes.KV6_CXX,
    Envelopes.KV6_DITP,
    Envelopes.KV6_EBS,
    Envelopes.KV6_GVB,
    Envelopes.KV6_RIG,
    Envelopes.KV6_QBUZZ,
]

def exit_handler():
    for ch in channels:
        print("Unsubscribing from %s" % ch)
        recv_sock.unsubscribe(ch)
    send_sock.close()
    context.destroy()


atexit.register(exit_handler)


context = zmq.Context.instance()
recv_sock = context.socket(socket_type=zmq.SUB)
recv_sock.connect(BISON)

# Publishing a merged stream of events on localhost:6505
send_sock = context.socket(socket_type=zmq.PUB)
send_sock.bind("tcp://*:%s" % 6505)

for ch in channels:
    recv_sock.subscribe(ch)

while True:
    topic = recv_sock.recv()
    print("Receiving from channel %s" % topic.decode("utf-8"))

    raw_compressed_response = recv_sock.recv()
    send_sock.send(topic)
    send_sock.send(raw_compressed_response)

