# Start the mongo docker container using:
# `docker run --name wdmov-mongo -p 27017:27017 -v ~/WDMOV/data/mongo-data:/data/db -d mongo`


import pymongo as mongo
import pandas  as pd

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.WDMOV

db.stops.remove()
stops_data = pd.read_csv("../data/gtfs-openov-nl/stops.txt")
stop_dicts = stops_data.to_dict(orient="records")



# Build the location in GeoJSON format to create an index on it
for stop in stop_dicts:
    stop["loc"] = { "type": "Point", "coordinates": [
        stop["stop_lon"],
        stop["stop_lat"]]
    }

db.stops.insert(stop_dicts)
db.stops.create_index([("stop_id", mongo.ASCENDING)])
db.stops.create_index([("loc", mongo.GEOSPHERE)])

db.routes.remove()
routes_data = pd.read_csv("../data/gtfs-openov-nl/routes.txt")
routes_dicts = routes_data.to_dict(orient="records")
db.routes.insert(routes_dicts)
db.routes.create_index([("route_id", mongo.ASCENDING),
                        ("route_short_name", mongo.ASCENDING)])
db.trips.remove()
trips_data = pd.read_csv("../data/gtfs-openov-nl/trips.txt")
trips_dicts = trips_data.to_dict(orient="records")
db.trips.insert(trips_dicts)
db.trips.create_index([("route_id", mongo.ASCENDING),
                       ("trip_id", mongo.ASCENDING)])


# This section takes a lot of time!
db.stop_times.remove()
stop_times = pd.read_csv("../data/gtfs-openov-nl/stop_times.txt")
for i in range(0, stop_times.shape[0], 100):
    stop_times_d = stop_times.iloc()[i:(i+100)].to_dict(orient="records")
    db.stop_times.insert(stop_times_d)

db.stop_times.create_index([("stop_id", mongo.ASCENDING)])

