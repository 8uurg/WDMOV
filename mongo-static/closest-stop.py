from pymongo import MongoClient
import time



client = MongoClient("localhost", 27017)
db = client.WDMOV

ewi_building = [4.373502, 51.998847]

start = time.time()
the_20_closest_stops_to_ewi = db.stops.find({
    "loc": {
        "$near": {
            "$geometry": {
                "type": "Point",
                "coordinates": ewi_building
            },
            "$maxDistance": 5000
        }
    }
}).limit(20)
end = time.time()
print("The query took %s milliseconds" % ((end - start)*1000))


for stop in the_20_closest_stops_to_ewi:
    print(stop)
