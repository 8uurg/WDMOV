# PostgreSQL

This folder contains the files for the PostgreSQL system.
Start up the DBMS using `docker-compose build && docker-compose up`

> Note, `docker-compose down` will delete the docker container, including the database data
> Do not run unless you want to reset the database.
> CTRL (or CMD) - C will nicely terminate the container without removing the data
> allowing you to start it up again without reinserting the data from where you were before. 

Queries and the dockerfile for PostgreSQL + PostGIS can be found in the folder `/database`.
`psql.bat` contains a command to quickly get a PSQL command line for entering queries into.

- Closest stop can be found in `nearest.sql`
- Average time between stops in `mean_stop_time_diff.sql`
- Next departure can be found in `nextstoptime.sql`

The data stream is requested and inserted by the code in `/stream-inserter`. 
- `buildy.bat` is a script that runs docker to build the container and name it `stream-inserter`.
- `runforalreadyrunningdb.bat` will launch the container into the dbs network, allowing it to access the database
  via the hostname `db`.
The queries on this stream are
- Next departure accounting for delays in `nextstoptimerealtime.sql`
- Current average delay in `averageortotaldelay.sql`. 
  This query is ran every 5 minutes by `interval-querier`. Structure of the folder is the same as `stream-inserter`. 