#!/bin/bash

set -e

echo "Stopping containers..."
docker kill inventoryserver || true

echo "Deleting containers..."
docker rm inventoryserver || true

sleep 1

echo "Starting server container..."
docker run --env-file env.env -d -p 1221:8080 --net inventory --name inventoryserver inventoryserver:latest
set +x

echo "To see logs of server, type 'docker logs -f inventoryserver'"
echo "View website at http://localhost:1221"
