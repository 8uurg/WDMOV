-- Before
ALTER TABLE stop_times ADD COLUMN arr_time timestamp;
UPDATE stop_times SET arr_time = current_date + arrival_time::interval;
-- Kinda important apparently.
SET TIME ZONE "Europe/Amsterdam";
-- Using just time gives an ERROR: date/time field value out of range: "24:50:22" (AAAAAAA)
-- Hence we have to do some stuff that takes a while.

-- For stop search.
SELECT * FROM stops as s JOIN stop_times as st ON s.stop_id = st.stop_id WHERE stop_name LIKE '%Mekelpark%';

-- It might be a good idea for this to create an index on stop_id.
CREATE INDEX idx_stop_times_stop_id ON stop_times (stop_id);
-- This takes a while and causes more space to be used.
-- Time: 41839.990 ms (00:41.840)


--
-- ALL 
--

-- FIND
SELECT stop_id, min(arr_time) FROM stop_times WHERE arr_time > now()::timestamp GROUP BY stop_id;

-- COLLECT MORE INFO.
SELECT t.trip_id, t.stop_id FROM 
    (SELECT stop_id, min(arr_time) as min_arr_time
     FROM stop_times 
     WHERE arr_time > now()
     GROUP BY stop_id) as s
    INNER JOIN stop_times AS t
    ON t.stop_id = s.stop_id
        AND
       t.arr_time = s.min_arr_time;
-- NO INDEX: Time: 22710.764 ms (00:22.711)
-- Index is not used when querying for all stops! (Time: 21729.752 ms (00:21.730))

--
-- Specific
-- 
SELECT t.trip_id, t.stop_id FROM 
    (SELECT stop_id, min(arr_time) as min_arr_time
     FROM stop_times 
     WHERE arr_time > now()
     GROUP BY stop_id) as ts
    INNER JOIN stop_times AS t
    ON t.stop_id = ts.stop_id
        AND
       t.arr_time = ts.min_arr_time
    JOIN stops as s ON ts.stop_id = s.stop_id
    WHERE s.stop_name LIKE '%Mekelpark%'; 
-- Time: 10104.501 ms (00:10.105)
SELECT t.trip_id, t.stop_id FROM 
    (SELECT s.stop_id, min(arr_time) as min_arr_time
     FROM stop_times as st
     JOIN stops as s ON st.stop_id = s.stop_id
     WHERE s.stop_name LIKE '%Mekelpark%' 
     AND   arr_time > now()
     GROUP BY s.stop_id
     ) as ts
    INNER JOIN stop_times AS t
    ON t.stop_id = ts.stop_id
        AND
       t.arr_time = ts.min_arr_time;
    
-- Time: 8.197 ms
SELECT t.trip_id, t.stop_id FROM 
    (SELECT s.stop_id, min(arr_time) as min_arr_time
     FROM stop_times as st
     JOIN stops as s ON st.stop_id = s.stop_id
     WHERE s.stop_name LIKE '%Mekelpark%' 
     AND   arr_time > now()
     GROUP BY s.stop_id
     ) as ts
    INNER JOIN stop_times AS t
    ON t.stop_id = ts.stop_id
        AND
       t.arr_time = ts.min_arr_time
    JOIN stops as s ON ts.stop_id = s.stop_id
    WHERE s.stop_name LIKE '%Mekelpark%'; 
-- Time: 7.579 ms