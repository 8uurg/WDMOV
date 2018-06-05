#!/bin/sh

echo 'Downloading GTFS OpenOV NL data'
mkdir data
cd data
wget http://gtfs.openov.nl/gtfs/gtfs-openov-nl.zip
unzip gtfs-openov-nl.zip -d .
rm gtfs-openov-nl.zip
cd ..
