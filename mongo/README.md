# Public Transit MongoDB

This folder contains the code for querying the public transit
data set using MongoDB.

Before performing any queries, download and unzip the most recent version of 
[gtfs-openov-nl.zip](http://gtfs.openov.nl/gtfs/gtfs-openov-nl.zip)
in the [data](../data/gtfs-openov-nl) folder at the root of this project.

Then set up a Docker instance of MongoDB using in the terminal:

```bash
docker run --name wdmov-mongo -p 27017:27017 -v /WDMOV/data/mongo-data:/data/db -d mongo
```

This will create the folder [data/mongo-data](../data/mongo-data) where 
Mongo stores its data.

Then run the script [`data-storage.py`](data-storage.py) to load all the data
into Mongo.

In the folder [static](./static) the code for querying the static data set 
can be found.

* [`closest-stop.py`](static/closest-stop.py) contains the code for finding 
the stop closest to a location. Currently the script looks for the stops 
closest to the TU Delft EWI building.
* [`avg-time-between-stops.py`](static/avg-time-between-stops.py) performs a
 MapReduce query to calculate the average time between stops during a journey.
* [`next-departure.py`](static/next-departure.py) lists the upcoming 
departures for the stops near EWI. 

In the folder [streaming](./streaming) the code for querying the data
stream can be found.

Before the query scripts can produce useful results, the data stream needs 
to be accessed. This is done by running [`inserter.py`](streaming/inserter
.py). This script automatically inserts the streaming data into Mongo which 
makes it available for the other queries.

* [`current-avg-delay.py`](streaming/current-avg-delay.py) calculates the 
current average delay every two seconds.
* [`next-departure-live.py`](streaming/next-departure-live.py) looks up the 
next departures from the stops near EWI and provides the current delay for 
each departure, if there is any. MongoDB cannot do arithmetic on dates, thus
 the new departure times should be calculated at the application level.