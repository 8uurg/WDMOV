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

-- TODO, query postgis style.