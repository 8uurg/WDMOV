--
-- ALL
--

-- Copy of original query.

SELECT t.trip_id, t.stop_id, s.min_arr_time FROM 
    (SELECT stop_id, min(arr_time) as min_arr_time
     FROM stop_times 
     WHERE arr_time > now()
     GROUP BY stop_id) as s
    INNER JOIN stop_times AS t
    ON t.stop_id = s.stop_id
        AND
       t.arr_time = s.min_arr_time;

-- Generate the realtime id.
SELECT dataownercode::text || ':' || lineplanningnumber::text || ':' || journeynumber::text as realtime_trip_id, ts.* FROM tripstatus as ts

-- Note: might want to turn this into something like a view, or something that is inserted into the db.

-- 
-- Note: Original query did not take into account the delays, making stuff a bit complicated for gathering more data.
--       Since having this data was 'nice-to-have' and not really required given the query, a simplified version
--       was tested instead.
-- SELECT t.trip_id, t.stop_id, s.min_arr_time, COALESCE(rtts.punctuality, 0) as delay FROM 
--     (SELECT stop_id, min(arr_time) as min_arr_time
--      FROM stop_times 
--      WHERE arr_time > now()
--      GROUP BY stop_id) as s
--     INNER JOIN stop_times AS t
--     ON t.stop_id = s.stop_id
--         AND
--        t.arr_time = s.min_arr_time
--     JOIN trips as tr ON tr.trip_id = t.trip_id 
--     LEFT JOIN 
--         -- We need the extra column. So subquery... Aaaaa.
--         (SELECT dataownercode::text || ':' || lineplanningnumber::text || ':' || journeynumber::text as realtime_trip_id, ts.* FROM tripstatus as ts)
--     as rtts
--     ON rtts.realtime_trip_id = tr.realtime_trip_id;

SELECT st.stop_id, min(arr_time - interval '1 second' * COALESCE(rtts.punctuality, 0)) as min_adj_arr_time, min(arr_time) as min_arr_time
     FROM stop_times as st
     JOIN trips as tr ON tr.trip_id = st.trip_id 
     LEFT JOIN 
        -- We need the extra column. So subquery... Aaaaa.
        (SELECT dataownercode::text || ':' || lineplanningnumber::text || ':' || journeynumber::text as realtime_trip_id, ts.* FROM tripstatus as ts)
     as rtts
     ON rtts.realtime_trip_id = tr.realtime_trip_id
     WHERE arr_time - interval '1 second' * COALESCE(rtts.punctuality, 0) > now()
     GROUP BY st.stop_id;

-- Current schema of real time info does not allow you to time travel (only the most recent is kept).    
-- Query was tested by making this a subquery and checking for  min_adj_arr_time <> min_arr_time.
-- 
-- This query requires the real time data inserter to be running.

-- Specific
SELECT s.stop_id, min(arr_time - interval '1 second' * COALESCE(rtts.punctuality, 0)) as min_adj_arr_time, min(arr_time) as min_arr_time
    FROM stop_times as st
    JOIN stops as s ON st.stop_id = s.stop_id
    JOIN trips as tr ON tr.trip_id = st.trip_id 
    LEFT JOIN 
        -- We need the extra column. So subquery... Aaaaa.
       (SELECT dataownercode::text || ':' || lineplanningnumber::text || ':' || journeynumber::text as realtime_trip_id, ts.* FROM tripstatus as ts)
    as rtts
    ON rtts.realtime_trip_id = tr.realtime_trip_id
    WHERE s.stop_name LIKE '%Mekelpark%' 
    AND   arr_time - interval '1 second' * COALESCE(rtts.punctuality, 0) > now()
    GROUP BY s.stop_id;