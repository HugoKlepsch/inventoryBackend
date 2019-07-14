#!/bin/bash

export BASE_DIR=$(pwd)

./server/sassCheck.sh

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install 8.11.4

npm install -g @vue/cli

python3 -m venv venv --system-site-packages

. venv/bin/activate

pip install Flask requests flask_sqlalchemy psycopg2

