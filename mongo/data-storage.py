import pymongo as mongo
import pandas  as pd
import datetime
import atexit
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.WDMOV

def exit_handler():
    client.close()


atexit.register(exit_handler)

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
    routes_data = pd.read_csv("../data/gtfs-openov-nl/routes.txt",
                              dtype={"route_id": str, "route_short_name": str})
    routes_dicts = routes_data.to_dict(orient="records")
    db.routes.insert(routes_dicts)
    db.routes.create_index([("route_id", mongo.ASCENDING)])
    db.routes.create_index([("route_short_name", mongo.ASCENDING)])


def import_trips():
    db.trips.drop()
    trips_data = pd.read_csv("../data/gtfs-openov-nl/trips.txt",
                             dtype={"route_id": str, "trip_id": str})
    trips_dicts = trips_data.to_dict(orient="records")
    db.trips.insert(trips_dicts)
    db.trips.create_index([("route_id", mongo.ASCENDING)])
    db.trips.create_index([("trip_id", mongo.ASCENDING)])


def import_stop_times():
    day = datetime.datetime.now()
    day = day.replace(hour=0, minute=0, second=0, microsecond=0)
    chunk_size = 200000
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
                             chunksize=chunk_size)

    i = 0
    for stop_time_chunk in stop_times:
        stop_times_dicts = stop_time_chunk.to_dict(orient="record")
        print("Iteration: %i" % i)

        db.stop_times.insert(stop_times_dicts)
        i += chunk_size

    print("Creating indices")
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


