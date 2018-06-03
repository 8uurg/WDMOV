SELECT AVG(b.arr_time - a.arr_time) FROM stop_times as a, stop_times as b WHERE a.trip_id = b.trip_id AND b.stop_sequence = a.stop_sequence + 1;

--        avg
-- -----------------
--  00:01:41.496678
-- (1 row)

-- Time: 70095.530 ms (01:10.096)

-- GROUPING BY trip_id gives 
-- Time: 78560.030 ms (01:18.560)
-- Turns out a lot of trips have a lot of small stops.
