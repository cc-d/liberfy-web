#!/bin/sh
ROOTDIR="$HOME/liberfy-web"
FRONTDIR="$ROOTDIR/libai-frontend"
APIDIR="$ROOTDIR/api"

echo $ROOTDIR $APIDIR $FRONTDIR
alias gentypes="npx openapi-typescript-codegen generate --exportSchemas true --input http://localhost:8888/openapi.json --output $FRONTDIR/src/api/"


npmapi() {
    gentypes
    cd $FRONTDIR && npm start
}


if [ -d "$HOME/.pyenv" ]; then
    pyenv local 3.11
fi

if [ -d "$HOME/.nvm" ]; then
    nvm use 20
fi
