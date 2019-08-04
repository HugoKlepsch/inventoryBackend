#!/bin/bash

export BASE_DIR=$(pwd)

cp git-hook-src/pre-push .git/hooks/pre-push

./server/sassCheck.sh

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install 8.11.4

npm install -g @vue/cli

pushd server/
npm install
popd

python3 -m venv venv

. venv/bin/activate

pip install -r server/requirements.txt

