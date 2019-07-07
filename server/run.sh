#!/bin/bash

set -x

echo "Running..."

echo "Waiting for database to be ready"
env
CONTINUE=1
while [ "$CONTINUE" -ne 0 ]; do
  sleep 1
  PGCONNECT_TIMEOUT=6 PGPASSWORD=$DBPASS psql -h $DBHOST --username=root -c "\d" inventorydb
  CONTINUE=$?
  echo "waiting..."
done
echo "Database ready"

#FLASK_APP=serverRun.py flask run --host='0.0.0.0' --port=8080
python serverRun.py

echo "Job failed, sleeping..."
while true; do
  sleep 1
done

echo "done"
