# Start the mongo docker container using:
# `docker run --name wdmov-mongo -p 27017:27017 -v ~/WDMOV/data/mongo-data:/data/db -d mongo`


import pymongo as mongo
import pandas  as pd
import datetime
import time

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.WDMOV

db.stops.drop()
stops_data = pd.read_csv("../data/gtfs-openov-nl/stops.txt")
stop_dicts = stops_data.to_dict(orient="records")

# Build the location in GeoJSON format to create an index on it
for stop in stop_dicts:
    stop["loc"] = { "type": "Point", "coordinates": [
        stop["stop_lon"],
        stop["stop_lat"]]
    }

db.stops.insert(stop_dicts)
db.stops.create_index([("stop_id", mongo.ASCENDING),
                       ("loc", mongo.GEOSPHERE)])

# db.routes.drop()
# routes_data = pd.read_csv("../data/gtfs-openov-nl/routes.txt")
# routes_dicts = routes_data.to_dict(orient="records")
# db.routes.insert(routes_dicts)
# db.routes.create_index([("route_id", mongo.ASCENDING),
#                         ("route_short_name", mongo.ASCENDING)])
# db.trips.drop()
# trips_data = pd.read_csv("../data/gtfs-openov-nl/trips.txt")
# trips_dicts = trips_data.to_dict(orient="records")
# db.trips.insert(trips_dicts)
# db.trips.create_index([("route_id", mongo.ASCENDING),
#                        ("trip_id", mongo.ASCENDING)])

day = datetime.datetime(year=2018, month=5, day=18)
def timestamp_to_date(timestamp):
    # Timestamps can be later than midnight, since it is the same operating
    # day.
    [h, m, s] = list(map(int, timestamp.split(":")))
    return day + datetime.timedelta(hours=h, minutes=m, seconds=s)

# This section takes a lot of time! +50min
print("Inserting stop times:")
db.stop_times.drop()
stop_times = pd.read_csv("../data/gtfs-openov-nl/stop_times.txt")
start = time.time()
for i in range(0, stop_times.shape[0]):
    stop_time = stop_times.iloc()[i].to_dict()
    if i % 5000 == 0:
        print("%f \% done" % (i / stop_times.shape[0]))

    # Convert the timestamps to datetime objects
    stop_time_d = stop_time
    stop_time_d["arrival_time"] = \
        timestamp_to_date(stop_time["arrival_time"])
    stop_time_d["departure_time"] = \
        timestamp_to_date(stop_time["departure_time"])

    db.stop_times.insert(stop_time_d)
    db.stops.update_one({"stop_id": stop_time_d["stop_id"]},
                        {"$push": {"stop_times": stop_time_d}})


db.stop_times.create_index([("stop_id", mongo.ASCENDING),
                            ("departure_time", mongo.ASCENDING),
                            ("trip_id", mongo.ASCENDING)])


