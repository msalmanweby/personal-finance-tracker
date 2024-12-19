from dotenv import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["DATABASE_NAME"]]

users_collection = db["users"]
expense_colection = db["expenses"]

