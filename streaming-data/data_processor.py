import zmq
import gzip
import atexit

context = zmq.Context.instance()
sock = context.socket(socket_type=zmq.SUB)
sock.connect("tcp://localhost:6505")
print("Connected")
sock.subscribe("") # Subscribe to all the things!


def exit_handler():
    print("Exiting data processor")
    sock.unsubscribe("")
    context.destroy()


atexit.register(exit_handler)

while True:
    topic = sock.recv() # Envelope
    raw_data = sock.recv()
    data = gzip.decompress(raw_data)
