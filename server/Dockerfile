FROM python:3.9-slim

WORKDIR /server

COPY ./src src
COPY ./server.py server.py

COPY ./setUp.sh setUp.sh
COPY ./start.sh start.sh

# RUN python -m pip install -U discord.py==1.7.3 
# RUN python -m pip install -U discord.py-self==1.9.2 
# RUN python -m pip install -U sqlalchemy 
# RUN python -m pip install -U psycopg2-binary 
# RUN python -m pip install -U flask
# RUN python -m pip install -U flask-restful 


RUN sh setUp.sh


CMD ["./.venv/bin/python", "server.py"]
