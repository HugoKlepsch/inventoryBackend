#!/bin/bash

set -e

echo "Building..."

echo "Compiling Sass into CSS..."
./sass/dart-sass/sass ./styles/style.scss ./static/css/styles.css

echo "done"
