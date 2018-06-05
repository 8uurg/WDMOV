--
-- Create tables
--
\timing

--
-- Configuration related to real time streaming data.
--
CREATE TABLE tripstatus (
    journeynumber integer,              -- journeynumber
    lineplanningnumber integer,         -- lineplanningnumber
    timestamp timestamp,                -- timestamp
    stop_id varchar(20),                -- either userstopcode or something the stop_id of the first stop.
                                        -- might be a foreign key, but I am extremely unsure
                                        -- as the documentation is unclear about this.
    punctuality int,                    -- punctuality in seconds.
                                        --  < 0 is ahead of schedule, > 0 is behind schedule, on schedule is = 0.
    status varchar(15),                 -- ARRIVAL, DELAY, DEPARTURE, ONROUTE, ONSTOP
    dataownercode varchar(10),           -- Which service provider is this status from?
    PRIMARY KEY(dataownercode, lineplanningnumber, journeynumber)
);
ALTER TABLE tripstatus OWNER TO postgres;
-- a lot of status versions have more data than the above table.
-- since we do not need it (punctuality is more important)
-- it is being thrown away. Probably useful for other things though.


CREATE TABLE routes (
    route_id integer PRIMARY KEY,
    agency_id text,
    route_short_name text,
    route_long_name text,
    route_desc text,
    route_type integer,
    route_color text,
    route_text_color text,
    route_url text
);
ALTER TABLE routes OWNER TO postgres;


CREATE TABLE stops (
    stop_id varchar(20) PRIMARY KEY, -- Turns out stop ids may have additional quantifiers before it, thus ain't a pure integer.
    stop_code real,
    stop_name text,
    stop_lat real,
    stop_lon real,
    location_type integer,
    parent_station text,
    stop_timezone text,
    wheelchair_boarding real,
    platform_code text
);
ALTER TABLE stops OWNER TO postgres;


CREATE TABLE trips (
    route_id integer references routes(route_id),
    service_id integer,
    trip_id integer PRIMARY KEY,
    realtime_trip_id text,
    trip_headsign text,
    trip_short_name text,
    trip_long_name text,
    direction_id integer,
    block_id real,
    shape_id real,
    wheelchair_accessible integer,
    bikes_allowed real
);
ALTER TABLE trips OWNER TO postgres;

CREATE TABLE stop_times (
    trip_id integer references trips(trip_id),
    stop_sequence integer,
    stop_id varchar(20) references stops(stop_id),
    stop_headsign text,
    arrival_time text, -- time
    departure_time text, -- time
    pickup_type integer,
    drop_off_type integer,
    timepoint integer,
    shape_dist_traveled real,
    fare_units_traveled integer,
    PRIMARY KEY(trip_id, stop_sequence, stop_id)
);
ALTER TABLE stop_times OWNER TO postgres;

--
-- Copy data to tables, uses psql commands.
--

\copy stops FROM '/data/stops.txt' csv header
\copy routes FROM '/data/routes.txt' csv header
\copy trips FROM '/data/trips.txt' csv header
\copy stop_times FROM '/data/stop_times.txt' csv header
-- COPY routes FROM '/data/routes.txt' WITH (format csv)
-- COPY stops FROM '/data/stops.txt' WITH (format csv)
-- COPY trips FROM '/data/trips.txt' WITH (format csv)
-- COPY stop_times FROM '/data/stop_times.txt' WITH (format csv)

--
-- Modify for postgis.
--

-- ALTER TABLE stops ADD COLUMN geom geography(Point, 4326);
-- UPDATE stops SET geom = ST_SetSrid(ST_MakePoint(stop_lon, stop_lat), 4326);
-- NOTE: this does not work before postgis is intialized in the DBMS.
--       so it will have to be intitialized at a later point.

--
-- For stop times. 
-- 

-- Arrival time is a string which is not easily copied formatted.
-- This could be done as preprocessing
ALTER TABLE stop_times ADD COLUMN arr_time timestamp;
UPDATE stop_times SET arr_time = current_date + arrival_time::interval;
-- UPDATE 16266327
-- Time: 1394917.932 ms (23:14.918)
-- Time measurements are for the Europe/Amsterdam timezone.
-- Default would otherwise be GMT, which would give wrong results. 
SET TIME ZONE "Europe/Amsterdam";

-- Indices other than primary keys are located in the sql files in which they are
-- used, or their own file.