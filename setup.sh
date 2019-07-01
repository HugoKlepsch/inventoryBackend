#!/bin/bash

python3 -m venv venv --system-site-packages

. venv/bin/activate

pip install --only-binary :all: mysqlclient
pip install Flask requests flask_sqlalchemy
