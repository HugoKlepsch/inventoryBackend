#!/bin/bash

echo "Running..."

while true; do
  sleep 1
  ping inventoryserver.inventory
  echo "sleeping"
done

echo "done"
