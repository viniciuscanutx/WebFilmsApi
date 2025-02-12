from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGO_DB_ACCESS = os.getenv("MONGO_DB_ACCESS")

conn = MongoClient(MONGO_DB_ACCESS)

db = conn.movies
dbc = conn.channels
dbs = conn.series
