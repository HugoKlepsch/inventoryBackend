#!/bin/bash

python -m venv venv --system-site-packages

. venv/bin/activate

pip install -r requirements.txt
