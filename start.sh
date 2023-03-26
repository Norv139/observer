#!/bin/bash

DIR=./.venv

if [ ! -d "$DIR" ]; then
    python3 -m venv .venv
    ./.venv/bin/python -m pip install -U discord.py==1.7.3
    ./.venv/bin/python -m pip install -U discord.py-self==1.9.2
fi

./.venv/bin/python main.py

