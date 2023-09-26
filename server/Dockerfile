FROM python:3.9-slim

WORKDIR /server

COPY ./src src
COPY ./server.py server.py

COPY ./setUp.sh setUp.sh
COPY ./start.sh start.sh

RUN sh setUp.sh

CMD ["./.venv/bin/python", "server.py"]