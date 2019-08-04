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

. /venv/bin/activate
cd server/
python -m api_src.api

echo "Job failed, sleeping..."
while true; do
  sleep 1
done

echo "done"
