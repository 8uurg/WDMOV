from datetime import timedelta
from datetime import datetime

import time

from pymongo import MongoClient
import atexit

client = MongoClient("localhost", 27017)
db = client.WDMOV

def exit_handler():
    client.close()


atexit.register(exit_handler)

current_avg_pipeline = [
    {
        "$match": {
            "last_update": {
                # According to the standard, every journey should update at
                # least once a minute, so we're playing it safe and discarding
                # any data older than 5 minutes
                "$gte": datetime.now() - timedelta(minutes=5)
            }
        }
    },
    {
        "$group": {
            "_id": None,
            "avg_punctuality": {
                "$avg": "$punctuality"
            }
        }
    }
]
while True:
    start = time.time()
    current_avg_time_result = \
        db.realtime.aggregate(current_avg_pipeline)
    end = time.time()
    current_avg_time = [r for r in current_avg_time_result][0][
        "avg_punctuality"]
    print("%s\tCurrent average delay:\t %f" % (
        datetime.now().strftime("%H:%M:%S"), current_avg_time
    ))
    time.sleep(2)
