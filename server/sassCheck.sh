#!/bin/bash

#DL sass
if [ ! -f ./sass/dart-sass/sass ]; then
    mkdir -p ./sass/
    curl -L https://github.com/sass/dart-sass/releases/download/1.22.3/dart-sass-1.22.3-linux-x64.tar.gz > ./sass/sass.tar.gz
    cd ./sass
    tar -xzvf ./sass.tar.gz
    rm ./sass.tar.gz
fi

