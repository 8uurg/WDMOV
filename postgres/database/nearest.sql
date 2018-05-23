
--
-- Using EarthDistance
--
WITH data AS (
    SELECT 
        stop_id, 
        stop_name, 
        earth_distance(ll_to_earth(stop_lat, stop_lon), ll_to_earth(51.99905, 4.3738)) as distance 
    FROM stops)
    SELECT * FROM data WHERE distance < 1000 ORDER BY distance ASC;

-- postgres=# WITH data AS (
--     SELECT
--         stop_id,
--         stop_name,
--         earth_distance(ll_to_earth(stop_lat, stop_lon), ll_to_earth(51.99905, 4.3738)) as distance
--     FROM stops)
--     SELECT * FROM data WHERE distance < 1000 ORDER BY distance ASC;
--      stop_id     |          stop_name           |     distance
-- -----------------+------------------------------+------------------
--  1099928         | Delft, TU Mekelpark          | 20.2675665059592
--  1217481         | Delft, TU - Mekelpark        | 31.0836392972462
--  1216986         | Delft, TU - Mekelpark        | 68.8227048681311
--  1099931         | Delft, TU Mekelpark          | 69.6594499683842
--  1216967         | Delft, TU - Aula             | 296.651442237827
--  1099926         | Delft, TU Aula               | 299.727446038034
--  1099933         | Delft, TU Sport & Cultuur    | 334.691411234174
--  stoparea:216295 | TU-Delft (NS-bus)            |  336.84435688722
--  743869          | TU-Delft (NS-bus)            |  336.84435688722
--  1238925         | Delft, TU - Sport en Cultuur | 338.297878621955
--  1217452         | Delft, TU - Aula             | 348.571994636965
--  1099929         | Delft, TU Aula               | 361.034151583759
--  1216926         | Delft, TU - Aula             | 378.534756237691
--  1217411         | Delft, TU - Aula             | 383.703802695054
--  1099930         | Delft, TU Sport & Cultuur    | 394.873138286924
--  1238807         | Delft, TU - Sport en Cultuur |  395.33330682153
--  1217537         | Delft, Schoemakerstraat      | 478.720413394411
--  1217000         | Delft, Schoemakerstraat      | 481.424219206779
--  1217141         | Delft, Prof. Krausstraat     | 660.935001589939
--  1217672         | Delft, Prof. Krausstraat     | 692.171678647565
--  1217558         | Delft, Julianalaan           | 699.748246201543
--  1100141         | Delft, Julianalaan           | 701.699491015006
--  1217075         | Delft, Julianalaan           | 713.103972998448
--  1100534         | Delft, Julianalaan           | 716.227991321317
--  1217339         | Delft, Michiel de Ruyterweg  | 783.143008675637
--  1217857         | Delft, Michiel de Ruyterweg  | 916.079727890399
--  1217830         | Delft, Poortlandplein        | 919.388946016133
--  1217146         | Delft, Koningin Emmalaan     | 927.752132217857
--  1217773         | Delft, Koningin Emmalaan     | 928.812284251079
--  1217236         | Delft, Poortlandplein        | 928.936351648902
--  1217209         | Delft, Nassauplein           | 940.355970781453
--  1217522         | Delft, TU - Kluyverpark      | 943.847864530744
--  558652          | Delft, TU Kluyverpark        | 946.901262686272
--  1217798         | Delft, Nassauplein           | 953.178748645404
--  1217460         | Delft, TU - Kluyverpark      | 954.095698271252
--  1099932         | Delft, TU Kluyverpark        | 958.076444283334
-- (36 rows)

-- Time: 523.545 ms

--
-- Using PostGIS.
--
SELECT stop_id, stop_name, ST_Distance(geom, ST_SetSRID(ST_Point(4.3738, 51.99905), 4326)) as distance FROM stops WHERE 
ST_DWithin(geom, ST_SetSRID(ST_Point(4.3738, 51.99905), 4326), 1000) 
ORDER BY distance;

-- postgres-# ORDER BY distance;
--      stop_id     |          stop_name           |   distance
-- -----------------+------------------------------+--------------
--  1099928         | Delft, TU Mekelpark          |  20.27332076
--  1217481         | Delft, TU - Mekelpark        |  31.10506518
--  1216986         | Delft, TU - Mekelpark        |  68.79019786
--  1099931         | Delft, TU Mekelpark          |  69.62648273
--  1216967         | Delft, TU - Aula             | 296.58626909
--  1099926         | Delft, TU Aula               | 299.67160474
--  1099933         | Delft, TU Sport & Cultuur    | 334.75351584
--  stoparea:216295 | TU-Delft (NS-bus)            |  336.7576073
--  743869          | TU-Delft (NS-bus)            |  336.7576073
--  1238925         | Delft, TU - Sport en Cultuur | 338.36124273
--  1217452         | Delft, TU - Aula             | 348.49758071
--  1099929         | Delft, TU Aula               |  360.9525816
--  1216926         | Delft, TU - Aula             | 378.40995379
--  1217411         | Delft, TU - Aula             | 383.58324815
--  1099930         | Delft, TU Sport & Cultuur    | 394.93906183
--  1238807         | Delft, TU - Sport en Cultuur | 395.41414704
--  1217537         | Delft, Schoemakerstraat      | 478.78898258
--  1217000         | Delft, Schoemakerstraat      | 481.48473981
--  1217141         | Delft, Prof. Krausstraat     | 661.32220297
--  1217672         | Delft, Prof. Krausstraat     | 692.63653579
--  1217558         | Delft, Julianalaan           | 699.70391382
--  1100141         | Delft, Julianalaan           | 701.64549691
--  1217075         | Delft, Julianalaan           | 713.06043318
--  1100534         | Delft, Julianalaan           | 716.17976301
--  1217339         | Delft, Michiel de Ruyterweg  | 783.05335361
--  1217857         | Delft, Michiel de Ruyterweg  | 915.90649922
--  1217830         | Delft, Poortlandplein        | 918.95438073
--  1217146         | Delft, Koningin Emmalaan     | 928.19579672
--  1217236         | Delft, Poortlandplein        |  928.5113318
--  1217773         | Delft, Koningin Emmalaan     | 929.23572626
--  1217209         | Delft, Nassauplein           | 940.35226731
--  1217522         | Delft, TU - Kluyverpark      | 943.90631658
--  558652          | Delft, TU Kluyverpark        | 946.96836984
--  1217798         | Delft, Nassauplein           | 953.15394065
--  1217460         | Delft, TU - Kluyverpark      | 954.15565541
--  1099932         | Delft, TU Kluyverpark        | 958.12569692
-- (36 rows)

-- Time: 17.862 ms

-- + With index

-- postgres=# CREATE INDEX loc_stops ON stops USING gist(geom);
-- CREATE INDEX
-- Time: 297.606 ms
-- postgres=# SELECT stop_id, stop_name, ST_Distance(geom, ST_SetSRID(ST_Point(4.3738, 51.99905), 4326)) as distance FROM stops WHERE
-- ST_DWithin(geom, ST_SetSRID(ST_Point(4.3738, 51.99905), 4326), 1000)
-- ORDER BY distance;
--      stop_id     |          stop_name           |   distance
-- -----------------+------------------------------+--------------
--  1099928         | Delft, TU Mekelpark          |  20.27332076
--  1217481         | Delft, TU - Mekelpark        |  31.10506518
--  1216986         | Delft, TU - Mekelpark        |  68.79019786
--  1099931         | Delft, TU Mekelpark          |  69.62648273
--  1216967         | Delft, TU - Aula             | 296.58626909
--  1099926         | Delft, TU Aula               | 299.67160474
--  1099933         | Delft, TU Sport & Cultuur    | 334.75351584
--  stoparea:216295 | TU-Delft (NS-bus)            |  336.7576073
--  743869          | TU-Delft (NS-bus)            |  336.7576073
--  1238925         | Delft, TU - Sport en Cultuur | 338.36124273
--  1217452         | Delft, TU - Aula             | 348.49758071
--  1099929         | Delft, TU Aula               |  360.9525816
--  1216926         | Delft, TU - Aula             | 378.40995379
--  1217411         | Delft, TU - Aula             | 383.58324815
--  1099930         | Delft, TU Sport & Cultuur    | 394.93906183
--  1238807         | Delft, TU - Sport en Cultuur | 395.41414704
--  1217537         | Delft, Schoemakerstraat      | 478.78898258
--  1217000         | Delft, Schoemakerstraat      | 481.48473981
--  1217141         | Delft, Prof. Krausstraat     | 661.32220297
--  1217672         | Delft, Prof. Krausstraat     | 692.63653579
--  1217558         | Delft, Julianalaan           | 699.70391382
--  1100141         | Delft, Julianalaan           | 701.64549691
--  1217075         | Delft, Julianalaan           | 713.06043318
--  1100534         | Delft, Julianalaan           | 716.17976301
--  1217339         | Delft, Michiel de Ruyterweg  | 783.05335361
--  1217857         | Delft, Michiel de Ruyterweg  | 915.90649922
--  1217830         | Delft, Poortlandplein        | 918.95438073
--  1217146         | Delft, Koningin Emmalaan     | 928.19579672
--  1217236         | Delft, Poortlandplein        |  928.5113318
--  1217773         | Delft, Koningin Emmalaan     | 929.23572626
--  1217209         | Delft, Nassauplein           | 940.35226731
--  1217522         | Delft, TU - Kluyverpark      | 943.90631658
--  558652          | Delft, TU Kluyverpark        | 946.96836984
--  1217798         | Delft, Nassauplein           | 953.15394065
--  1217460         | Delft, TU - Kluyverpark      | 954.15565541
--  1099932         | Delft, TU Kluyverpark        | 958.12569692
-- (36 rows)

-- Time: 1.153 ms