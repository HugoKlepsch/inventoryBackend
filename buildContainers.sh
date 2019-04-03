#!/bin/bash

set -e 
set -x

echo "Building..."

docker build -t inventorydb:latest db/

docker build -t inventoryserver:latest server/

echo "done"
