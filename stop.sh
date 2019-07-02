#!/bin/bash

set -e

echo "Stopping containers..."

docker kill inventorydb inventoryserver || true

echo "Deleting containers..."
docker rm inventorydb inventoryserver || true

echo "Deleting network..."
docker network prune -f

echo "done"
