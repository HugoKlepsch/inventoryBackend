#!/bin/bash

set -e

sass_dir="$BASE_DIR/server/sass"

#DL sass
if [ ! -f "$sass_dir/dart-sass/sass" ]; then
    mkdir -p "$sass_dir"
    curl -L https://github.com/sass/dart-sass/releases/download/1.22.3/dart-sass-1.22.3-linux-x64.tar.gz > $sass_dir/sass.tar.gz
    cd "$sass_dir"
    tar -xzvf ./sass.tar.gz
    rm ./sass.tar.gz
fi

