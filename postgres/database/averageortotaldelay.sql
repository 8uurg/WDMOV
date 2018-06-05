-- Current delay, ahead of schedule to 0.
SELECT avg(CASE WHEN punctuality > 0 THEN punctuality ELSE 0 END) 
FROM tripstatus 
WHERE punctuality IS NOT NULL 
AND timestamp > now() - interval '5 minutes';
--          avg
-- ---------------------
--  47.9385714285714286
-- (1 row)

-- Time: 0.489 ms


-- Current average punctuality.
SELECT avg(punctuality) FROM tripstatus WHERE punctuality IS NOT NULL;
--          avg
-- ----------------------
--  -53.1042857142857143
-- (1 row)

-- Time: 0.421 ms

-- Some other similar queries.
SELECT max(punctuality) FROM tripstatus WHERE punctuality IS NOT NULL;
--  max
-- ------
--  1834
-- (1 row)
-- Time: 0.496 ms

-- Yep, that is a delay of over 30 minutes!