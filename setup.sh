#!/bin/bash

python -m venv venv --system-site-packages

. venv/bin/activate

pip install Flask requests mysqlclient flask_sqlalchemy
