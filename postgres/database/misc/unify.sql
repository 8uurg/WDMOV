--
-- A fun query that tries to find out what stops can maybe be merged.
-- Not actually used, but still interesting. Left it here for people
-- to enjoy and look at.
--

SELECT a.stop_id, a.stop_name, b.stop_id, b.stop_name, 
    earth_distance(ll_to_earth(a.stop_lat, a.stop_lon), 
                   ll_to_earth(b.stop_lat, b.stop_lon)) 
    as distance 
FROM stops as a, stops as b 
WHERE 
    levenshtein_less_equal(a.stop_name, b.stop_name, 3) < 3 
    AND a.stop_name <> b.stop_name 
    AND a.stop_id < b.stop_id 
ORDER BY distance 
LIMIT 10;

-- Maybe TODO, query postgis style, because this is slow.