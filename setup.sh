#!/bin/bash

./server/sassCheck.sh

python3 -m venv venv --system-site-packages

. venv/bin/activate

pip install Flask requests flask_sqlalchemy
