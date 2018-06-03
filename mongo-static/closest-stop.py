from pymongo import MongoClient
import time



client = MongoClient("localhost", 27017)
db = client.WDMOV

ewi_building = [4.373502, 51.998847]

the_20_closest_stops_to_ewi_perf = db.stops.find({
    "loc": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": ewi_building
            },
            "$maxDistance": 5000
        }
    }
}).limit(20).explain()["executionStats"]

print("Querying for the 20 closests stop to the EWI building takes: %f ms" %
        the_20_closest_stops_to_ewi_perf["executionTimeMillis"])
