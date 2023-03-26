#!/bin/bash

VERSION=$(pm2 -v)
yarn global add pm2

DIR=./.venv

if [ ! -d "$DIR" ]; then
    python3 -m venv .venv
    ./.venv/bin/python -m pip install -U discord.py==1.7.3
    ./.venv/bin/python -m pip install -U discord.py-self==1.9.2
fi

source ./.venv/bin/activate

pm2 start

echo "
pm2 start - for start
pm2 kill - for stop
pm2 monit - for monitoring
"

