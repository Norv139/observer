#!/bin/bash bash

DIR=./.venv

REQ=$(cat ./req.txt)

FRM=$(./.venv/bin/python -m pip freeze)

if [ ! -d "$DIR" ]; then
    echo "install"
    python3 -m venv .venv
fi

for item in ${REQ}; do
    if echo $FRM | grep -qw -i "$item"; then
        echo "+ $item"
    else
        # echo "- $item"
        ./.venv/bin/python -m pip install -U $item
    fi
done