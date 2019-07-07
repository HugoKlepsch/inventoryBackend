#!/bin/bash

set -e

echo "Building..."
echo "Compiling Sass into CSS..."
echo `pwd`
./sass/dart-sass/sass ./static/sass/style.scss ./static/css/styles.css

echo "WIP - WIP"

echo "done"
