#!/bin/bash

cd ${BASE_DIR}/server && python -m pylint --rcfile .pylintrc api_src
