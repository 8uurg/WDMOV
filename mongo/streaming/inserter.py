import zmq
import gzip
import atexit
import pymongo as mongo
from datetime import datetime

from const import Envelopes, BISON
from bs4 import BeautifulSoup
from pymongo import MongoClient




channels = [
    Envelopes.KV6_ARR,
    Envelopes.KV6_CXX,
    Envelopes.KV6_DITP,
    Envelopes.KV6_EBS,
    Envelopes.KV6_GVB,
    Envelopes.KV6_RIG,
    Envelopes.KV6_QBUZZ,
]

client = MongoClient("localhost", 27017)
db = client.WDMOV

db.realtime.drop()
db.realtime.create_index([("realtime_trip_id", mongo.DESCENDING)])

realtime = db.realtime



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
    client.close()


atexit.register(exit_handler)

while True:
    topic = sock.recv() # Envelope
    raw_data = sock.recv()
    data = gzip.decompress(raw_data)
    soup = BeautifulSoup(data, features="lxml-xml")
    posinfo = soup.find('VV_TM_PUSH')
    if posinfo is None:
        continue
    posinfo = posinfo.find('KV6posinfo')
    if posinfo is None:
        continue
    for vinfo in posinfo.find_all(recursive=False):
        status = vinfo.name
        journey_number = vinfo.find('journeynumber').text
        line_planning_number = vinfo.find('lineplanningnumber').text
        timestamp_s = vinfo.find('timestamp').text
        stop_id = vinfo.find('userstopcode')
        stop_id = None if stop_id is None else stop_id.text
        data_owner_code = vinfo.find('dataownercode').text
        punctuality = vinfo.find('punctuality')
        punctuality = None if punctuality is None else punctuality.text
        print(f"[{timestamp_s}] Journey {journey_number} [{line_planning_number}] is now {status} at {stop_id}, it is currently {punctuality} s behind schedule.")

        if status == "END":
            realtime.delete_one({"realtime_trip_id": realtime_trip_id})
            continue

        if punctuality is None:
            continue

        realtime_trip_id = "%s:%s:%s" % (data_owner_code, line_planning_number,
                                         journey_number)
        timestamp = datetime.strptime(timestamp_s[0:19], '%Y-%m-%dT%H:%M:%S')

        data = {
            "realtime_trip_id": realtime_trip_id,
            "punctuality": int(punctuality),
            "last_update": timestamp
        }
        realtime.update({
            "realtime_trip_id": realtime_trip_id
        }, data, True)
