#!/bin/bash

python -m venv venv --system-site-packages

. venv/bin/activate

pip install Flask psycopg2-binary requests mysqlclient
