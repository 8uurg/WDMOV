#!/bin/sh

echo '[1] Stopping all Docker containers'
docker stop $(docker ps -a -q)

echo '[2] Removing all Docker containers'
docker rm $(docker ps -a -q)
