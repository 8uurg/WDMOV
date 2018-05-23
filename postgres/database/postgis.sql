-- Update DB for use with postgis lookups.
ALTER TABLE stops ADD COLUMN geom geography(Point, 4326);
UPDATE stops SET geom = ST_SetSrid(ST_MakePoint(stop_lon, stop_lat), 4326);