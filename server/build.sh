#!/bin/bash

set -e

echo "Building..."

echo "Compiling Sass into CSS..."
./sass/dart-sass/sass ./styles/style.scss ./public/css/styles.css

echo "Compiling Vue"
. "$NVM_DIR/nvm.sh"
npm run build-dev
cp -r ./dist/* public/

echo "done"
