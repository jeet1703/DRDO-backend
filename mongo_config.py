# File: backend/mongo_config.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["drdo_portal"]
records_collection = db["records"]