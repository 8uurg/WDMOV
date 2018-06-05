# Initial version from streaming-data/data_processor.py
# Together with streaming-data/merger.py

import zmq
import gzip
import atexit
from const import Envelopes, BISON
from bs4 import BeautifulSoup
import psycopg2
import iso8601 # Dates, I would have preferred the fruit over this.

channels = [
    Envelopes.KV6_ARR,
    Envelopes.KV6_CXX,
    Envelopes.KV6_DITP,
    Envelopes.KV6_EBS,
    Envelopes.KV6_GVB,
    Envelopes.KV6_RIG,
    Envelopes.KV6_QBUZZ,
]

conn = psycopg2.connect(user="postgres", host="db")

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

currcur = None

def begin_batch():
    global currcur
    currcur = conn.cursor()

def process(journeynumber, lineplanningnumber, timestamp, 
             stop_id, punctuality, status, dataownercode):
    global currcur
    # Special query! Uses a concept usually described as upsert.
    # Used the following to iron out the details.
    # https://stackoverflow.com/questions/40572126/possible-to-upsert-in-postgres-on-conflict-on-exactly-one-of-2-columns
    currcur.execute("""INSERT INTO tripstatus (journeynumber, lineplanningnumber, timestamp, stop_id, punctuality, status, dataownercode) 
                       VALUES (%s,%s,%s,%s,%s,%s,%s) 
                       ON CONFLICT (dataownercode, lineplanningnumber, journeynumber)
                       DO UPDATE SET
                            timestamp     = EXCLUDED.timestamp, 
                            stop_id       = EXCLUDED.stop_id, 
                            punctuality   = EXCLUDED.punctuality, 
                            status        = EXCLUDED.status, 
                            dataownercode = EXCLUDED.dataownercode
                        WHERE
                            tripstatus.timestamp < EXCLUDED.timestamp
                       ;""", 
                       (journeynumber, lineplanningnumber, timestamp, stop_id, punctuality, status, dataownercode))

def finish_batch():
    global conn
    global currcur
    conn.commit()
    currcur.close()
# def insert_into_db(journeynumber, lineplanningnumber, timestamp, 
#             stop_id, punctuality, status, dataownercode):
#     # perform an UPSERT: insert if value with the primary key exists yet.
#     # otherwise update entry with the key!
#     conn.execute("INSERT INTO tripstatus VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO UPDATE;")

atexit.register(exit_handler)

while True:
    topic = sock.recv() # Envelope
    raw_data = sock.recv()
    data = gzip.decompress(raw_data)
    print("Recieved message on {}".format(topic))
    # print(data)
    soup = BeautifulSoup(data, features="xml")
    posinfo = soup.find('VV_TM_PUSH')
    if posinfo is None: 
        continue
    posinfo = posinfo.find('KV6posinfo')
    if posinfo is None: 
        continue
    begin_batch()
    for vinfo in posinfo.find_all(recursive=False):
        status = vinfo.name
        journeynumber = vinfo.find('journeynumber').text
        lineplanningnumber = vinfo.find('lineplanningnumber').text
        timestamp = vinfo.find('timestamp').text
        stop_id = vinfo.find('userstopcode')
        stop_id = None if stop_id is None else stop_id.text
        dataownercode = vinfo.find('dataownercode').text
        punctuality = vinfo.find('punctuality')
        punctuality = None if punctuality is None else punctuality.text
        parsed_timestamp = iso8601.parse_date(timestamp)
        print(f"[{parsed_timestamp}] Journey {journeynumber} [{lineplanningnumber}] is now {status} at {stop_id}, it is currently {punctuality} s behind schedule.")
        process(journeynumber, lineplanningnumber, parsed_timestamp, 
             stop_id, punctuality, status, dataownercode)
    finish_batch()

