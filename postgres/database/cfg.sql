--
-- Create tables
--

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