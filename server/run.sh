#!/bin/bash

echo "Running..."

CONTINUE=1
while [ "$CONTINUE" -ne 0 ]; do
  sleep 1
  echo "connecting"
  mysql -h inventorydb.inventory -u root --password=notwaterloo -e "SELECT * FROM ACCOUNT_INFO;" inventorydb
  CONTINUE=$?
done

echo "Connected"

uwsgi --socket 0.0.0.0:8080 --protocol=http -w main:app

echo "Job failed, sleeping..."
while true; do
  sleep 1
done

echo "done"
