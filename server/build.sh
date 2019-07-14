#!/bin/bash

set -e

echo "Building..."

echo "Compiling Sass into CSS..."
./sass/dart-sass/sass ./styles/style.scss ./static/css/styles.css

echo "Compiling Vue"
cd ./vue
. "$NVM_DIR/nvm.sh"
npm run build
cp ./dist/css/* ../static/css/
cp ./dist/img/* ../static/img/
cp ./dist/js/* ../static/js/
cp ./dist/index.html ../static/index.html

echo "done"
