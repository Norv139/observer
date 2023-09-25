#!/bin/bash

DIR=./.venv

# REQ=( discord.py==1.7.3 discord.py-self==1.9.2 sqlalchemy psycopg2-binary flask flask-restful )

FRM=$(./.venv/bin/python -m pip freeze)

if [ ! -d "$DIR" ]; then
    echo "install"
    python3 -m venv .venv
fi

./.venv/bin/python -m pip install -U discord.py==1.7.3 
./.venv/bin/python -m pip install -U discord.py-self==1.9.2 
./.venv/bin/python -m pip install -U sqlalchemy 
./.venv/bin/python -m pip install -U psycopg2-binary 
./.venv/bin/python -m pip install -U flask
./.venv/bin/python -m pip install -U flask-restful 

# for item in "${REQ[@]}"; do
#     if echo $FRM | grep -qw -i "$item"; then
#         echo "+ $item"
#     else
#         ./.venv/bin/python -m pip install -U $item
#     fi
# done