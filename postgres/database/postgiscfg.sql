-- Update DB for use with postgis lookups.
ALTER TABLE stops ADD COLUMN geom geography(Point, 4326);
UPDATE stops SET geom = ST_SetSrid(ST_MakePoint(stop_lon, stop_lat), 4326);

-- Needs to be manually ran after the database setup.
-- Cannot add a column with the geography type using the normal init as postgis is not initialized yet.