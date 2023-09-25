#!/bin/bash

DIR=./.venv

REQ=(
    discord.py==1.7.3 
    discord.py-self==1.9.2 
    sqlalchemy 
    psycopg2-binary 
    flask
    flask-restful 
)

FRM=$(./.venv/bin/python -m pip freeze)

if [ ! -d "$DIR" ]; then
    echo "install"
    python3 -m venv .venv
fi

for item in "${REQ[@]}"; do
    if echo $FRM | grep -qw -i "$item"; then
        echo "+ $item"
    else
        ./.venv/bin/python -m pip install -U $item
    fi
done