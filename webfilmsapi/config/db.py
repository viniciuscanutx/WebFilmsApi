import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

ca = certifi.where()

MONGO_DB_ACCESS = os.getenv("MONGO_DB_ACCESS")

conn = MongoClient(MONGO_DB_ACCESS, tlsCAFile=ca)

db = conn.webfilmsapi
