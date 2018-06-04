from datetime import datetime

from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.WDMOV

ewi_building = [4.373502, 51.998847]

current_location = ewi_building
maximum_departures = 10
current_time = datetime(year=2018, month=5, day=18, hour=15, minute=30)

stops_near_current_location = db.stops.find({
    "loc": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": current_location
            },
            "$maxDistance": 250
        }
    },
    "stop_times": {
        "departure_time": {"$gte": current_time }
    }
})

next_departures = stops_near_current_location\
    .aggregate([
        {"$unwind": "$stop_times"}, # Extract the stop times from the stops
        {"$sort": {"$departure_time": 1}},
        {"$limit": maximum_departures}
    ])

for departure in next_departures:
    print(departure)
