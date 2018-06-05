from datetime import datetime

from pymongo import MongoClient
import atexit

client = MongoClient("localhost", 27017)
db = client.WDMOV

def exit_handler():
    client.close()


atexit.register(exit_handler)

ewi_building = [4.373502, 51.998847]

current_location = ewi_building
maximum_departures = 10
current_time = datetime.now()
current_time = current_time.replace(hour=17, minute=5, second=0,
                                    microsecond=0)

next_departure_with_delay_pipeline = [
    { # Find the nearest stops
       "$geoNear": {
           "spherical": True,
           "maxDistance": 250,
           "limit": 10,
           "near": {
                "type": "Point",
                "coordinates": current_location
           },
           "distanceField": "distance"
       }
    },
    { # Join with the stop_times associated with the stops
        "$lookup": {
            "from": "stop_times",
            "localField": "stop_id",
            "foreignField": "stop_id",
            "as": "time"
        }
    },
    { # Extract the stop times
        "$unwind": "$time"
    },
    { # Filter the stop times in the past
        "$match": {
            "time.departure_time": {
                "$gt": current_time
            }
        }
    },
    { # Sort them by ascending order, so that earliest stop times are on top
        "$sort": {"time.departure_time": 1}
    },
    { # Limit the maximum number of fields (because sort is right before limit
        # the query can be optimized more).
        "$limit": maximum_departures
    },
    { # Lookup the realtime_trip_id
        "$lookup": {
            "from": "trips",
            "localField": "time.trip_id",
            "foreignField": "trip_id",
            "as": "trip"
        }
    },
    {
        "$unwind": "$trip"
    },
    { # Lookup the realtime data, if it exists
        "$lookup": {
            "from": "realtime",
            "localField": "trip.realtime_trip_id",
            "foreignField": "realtime_trip_id",
            "as": "realtime"
        }
    }
    ]


# runtimes = []
# for i in range(0, 200):
#     start = time()
#     db.stops.aggregate(next_departure_with_delay_pipeline)
#     end = time()
#     runtimes.append((end - start) * 1000)

# print(runtimes)
# print("On average the query takes: %f ms" % (sum(runtimes)/len(runtimes)))

for departure in db.stops.aggregate(next_departure_with_delay_pipeline):
    print(departure)