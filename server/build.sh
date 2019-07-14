#!/bin/bash

set -e

echo "Building..."

echo "Compiling Sass into CSS..."
./sass/dart-sass/sass ./styles/style.scss ./public/css/styles.css

echo "Compiling Vue"
. "$NVM_DIR/nvm.sh"
npm run build
cp ./dist/css/* public/css/
cp ./dist/img/* public/img/
cp ./dist/js/* public/js/
cp ./dist/index.html public/index.html

echo "done"
