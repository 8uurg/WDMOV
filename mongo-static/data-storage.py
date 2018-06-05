# Start the mongo docker container using:
# `docker run --name wdmov-mongo -p 27017:27017 -v ~/WDMOV/data/mongo-data:/data/db -d mongo`


import pymongo as mongo
import pandas  as pd
import datetime

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.WDMOV


def import_stops():
    db.stops.drop()
    stops_data = pd.read_csv("../data/gtfs-openov-nl/stops.txt",
                             dtype={"stop_id": str},)
    stop_dicts = stops_data.to_dict(orient="records")

    # Build the location in GeoJSON format to create an index on it
    for stop in stop_dicts:
        stop["loc"] = {"type": "Point", "coordinates": [
            stop["stop_lon"],
            stop["stop_lat"]]
        }
        stop["stop_id"] = str(stop["stop_id"])

    db.stops.insert(stop_dicts)
    db.stops.create_index([("stop_id", mongo.ASCENDING)])
    db.stops.create_index([("loc", mongo.GEOSPHERE)])


def import_routes():
    db.routes.drop()
    routes_data = pd.read_csv("../data/gtfs-openov-nl/routes.txt")
    routes_dicts = routes_data.to_dict(orient="records")
    db.routes.insert(routes_dicts)
    db.routes.create_index([("route_id", mongo.ASCENDING)])
    db.routes.create_index([("route_short_name", mongo.ASCENDING)])


def import_trips():
    db.trips.drop()
    trips_data = pd.read_csv("../data/gtfs-openov-nl/trips.txt")
    trips_dicts = trips_data.to_dict(orient="records")
    db.trips.insert(trips_dicts)
    db.trips.create_index([("route_id", mongo.ASCENDING)])
    db.trips.create_index([("trip_id", mongo.ASCENDING)])


def import_stop_times():
    day = datetime.datetime(year=2018, month=6, day=4)

    def timestamp_to_date(timestamp):
        # Timestamps can be later than midnight, since it is the same operating
        # day.
        [h, m, s] = list(map(int, timestamp.split(":")))
        return day + datetime.timedelta(hours=h, minutes=m, seconds=s)

    # This section takes a lot of time! +30min
    db.stop_times.drop()
    stop_times = pd.read_csv("../data/gtfs-openov-nl/stop_times.txt",
                             dtype={"stop_id": str, "trip_id": str},
                             parse_dates=["arrival_time", "departure_time"],
                             date_parser=timestamp_to_date,
                             chunksize=20000)
    i = 0
    for stop_time_chunk in stop_times:

        stop_times_dicts = stop_time_chunk.to_dict(orient="record")
        if i % 100000 == 0:
            print(stop_times_dicts[0])
            print("Iteration: %i" % i)

        db.stop_times.insert(stop_times_dicts)
        i += 20000

    db.stop_times.create_index([("stop_id", mongo.ASCENDING)])
    db.stop_times.create_index([("departure_time", mongo.ASCENDING)])
    db.stop_times.create_index([("trip_id", mongo.ASCENDING)])


if input("Do you want to import stops? \"yes\"?") == "yes":
    import_stops()

if input("Import stop times? \"yes\"?") == "yes":
    import_stop_times()

if input("Import routes? \"yes\"?") == "yes":
    import_routes()

if input("Import trips? \"yes\"?") == "yes":
    import_trips()


