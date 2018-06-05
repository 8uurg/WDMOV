WDMOV
-----

This is the code / repository for using the public transport data from https://openov.nl

We have investigated three systems: 
 - PostgreSQL (a relational database) in `/postgres`
 - MongoDB (a document store) in `/mongo`
 - Apache Kafka (Streaming) in `missing?`

In order to work with these systems data is required.
For convienience `getdata.sh` will automatically download and unpack this to `/data`.

Additional documentation may be available in the subfolders.