#!/bin/bash

echo "Running..."

echo "Waiting for database to be ready"
CONTINUE=1
while [ "$CONTINUE" -ne 0 ]; do
  sleep 1
  PGPASSWORD=$DBPASS psql -h $DBHOST --username=root -c "\d" inventorydb
  CONTINUE=$?
done
echo "Database ready"

#FLASK_APP=serverRun.py flask run --host='0.0.0.0' --port=8080
python serverRun.py

echo "Job failed, sleeping..."
while true; do
  sleep 1
done

echo "done"
