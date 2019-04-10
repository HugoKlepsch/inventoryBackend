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

FLASK_APP=serverRun.py flask run --host='0.0.0.0' --port=8080

echo "Job failed, sleeping..."
while true; do
  sleep 1
done

echo "done"
