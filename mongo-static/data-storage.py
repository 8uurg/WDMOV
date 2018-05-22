# Start the mongo docker container using:
# `docker run --name wdmov-mongo -p 27017:27017 -v ~/Developer/WDMOV/data/mongo-data:/data/db -d mongo`


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
