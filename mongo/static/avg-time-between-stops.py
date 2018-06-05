from time import time
from bson.code import Code
import atexit

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.WDMOV

def exit_handler():
    client.close()


atexit.register(exit_handler)

map_group_trips = \
    Code("""
        function() {
            emit(this.trip_id, {
                seq_num: this.stop_sequence,
                arrival: this.arrival_time,
                departure: this.departure_time
            });
        } 
    """)

reduce_sort = \
    Code("""
        function(trip, times) {
            times.slice().sort((a, b) => a.seq_num - b.seq_num)
            return times;
        }
    """)

# Gets a dictionary with a trip id and a dictionary with stop_info
# sequence num, arrival time and departure times.
map_calculate_avg_times_per_trip = \
    Code("""
        function() {
            const stop_times = this.value.stop_times;
            emit(0, stop_times);
            return;
            if (stop_times && stop_times.length > 1){
                var avg = 0.0;
                for(i = 1; i < stop_times.length; i++) {
                    avg = (i-1)/i * avg 
                             + 1/i * (
                             (stop_times[i]["arrival"] 
                            - stop_times[i-1]["departure"])/1000);
                }
                emit(0, avg);
            }
        }
    """)

reduce_overall_avg = \
    Code("""
        function(key, avgs) {
            return Array.sum(avgs)/avgs.length
        }
    """)

if input("Are you sure you want to drop the group_trips? "
         "Enter \"yes\" if so.") == "yes":
    db.group_trips.drop()
    group_trips = None
else:
    group_trips = db.group_trips

db.calculate_avg_time_between_stops.drop()
start = time()

db.selected_trips = db.stop_times.find({})

if group_trips is None:
    group_trips = db.limited_stop_times\
        .map_reduce(map_group_trips, reduce_sort, "group_trips")

avg_time_between_stops_result = group_trips\
    .map_reduce(map_calculate_avg_times_per_trip, reduce_overall_avg,
                "calculate_avg_time_between_stops")

avg_time_between_stops = avg_time_between_stops_result.find()
end = time()

print("The average time between stops is: %s seconds" % avg_time_between_stops)
print("The query took %f seconds" % (end-start))