#!/bin/bash

set -e

./stop.sh 

echo "Pruning old docker network..."
docker network prune -f

echo "Creating docker network..."
docker network create inventory

echo "Starting db container..."
docker run -d -p 3301:3306 --net inventory --name inventorydb inventorydb:latest --default-authentication-plugin=mysql_native_password

echo "Starting server container..."
docker run --env-file server/env.env -d -p 1221:8080 --net inventory --name inventoryserver inventoryserver:latest
set +x

echo "To see logs of db, type 'docker logs -f inventorydb'"
echo "To see logs of server, type 'docker logs -f inventoryserver'"
echo "View website at http://localhost:1221"

