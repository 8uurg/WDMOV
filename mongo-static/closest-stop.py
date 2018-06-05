from pymongo import MongoClient
import time



client = MongoClient("localhost", 27017)
db = client.WDMOV

ewi_building = [4.373502, 51.998847]

runtimes = []

for i in range(0, 200):
    runtime = db.stops.find({
        "loc": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": ewi_building
                }
            }
        }
    }).limit(20).explain()["executionStats"]["executionTimeMillis"]
    runtimes.append(runtime)


# On average around 1.5ms
print("On average the query takes: %f" % (sum(runtimes)/len(runtimes)))


