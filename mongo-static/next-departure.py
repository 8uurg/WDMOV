from datetime import datetime

from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.WDMOV

ewi_building = [4.373502, 51.998847]

current_location = ewi_building
maximum_departures = 10
current_time = datetime(year=2018, month=6, day=4, hour=15, minute=30)


next_departures = db.stops\
    .aggregate([
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
    }
    ])

print("Next departures:")
for departure in next_departures:
    print(departure)
