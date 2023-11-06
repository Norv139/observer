
from src.observer import Observer
from sqlalchemy import URL
import json
import os


# from src.fetchInfo import get_token

with open('settings.json') as f:
  SETTINGS = json.load(f)

DB_NAME = os.getenv('DB_NAME') or 'cloud_db'
DB_USER = os.getenv('DB_USER') or "admin_cloud"
DB_PASS = os.getenv('DB_PASS') or "admin"
DB_PORT = os.getenv('DB_PORT') or 5432
DB_HOST = os.getenv('DB_HOST') or "localhost"

TOKEN = SETTINGS["token"] or []
TARGET = SETTINGS["target"] or []
IGNOR = SETTINGS["ignor"] or []

url = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT,
    host=DB_HOST,
)



observer = Observer(
    connect_url=url,
    ignor_list=IGNOR,
    target_list=TARGET
)
observer.run(TOKEN)