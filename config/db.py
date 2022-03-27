from pymongo import MongoClient
import os
MONGO_URL = os.environ.get("MONGO_URL")
con = MongoClient(MONGO_URL)
db = con.test
