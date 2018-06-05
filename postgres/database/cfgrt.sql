--
-- Configuration related to real time streaming data.
--
CREATE TABLE tripstatus (
    journeynumber integer PRIMARY KEY,  -- journeynumber
    lineplanningnumber integer,         -- lineplanningnumber
    timestamp timestamp,                -- timestamp
    stop_id varchar(20),                -- either userstopcode or something the stop_id of the first stop.
                                        -- might be a foreign key, but I am extremely unsure
                                        -- as the documentation is unclear about this.
    punctuality int,                    -- punctuality in seconds.
                                        --  < 0 is ahead of schedule, > 0 is behind schedule, on schedule is = 0.
    status varchar(15),                 -- ARRIVAL, DELAY, DEPARTURE, ONROUTE, ONSTOP
    dataownercode varchar(10)           -- Which service provider is this status from?
);
-- a lot of status versions have more data than the above table.
-- since we do not need it (punctuality is more important)
-- it is being thrown away. Probably useful for other things though.