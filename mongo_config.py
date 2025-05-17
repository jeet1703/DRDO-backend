# File: backend/mongo_config.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["drdo_portal"]
records_collection = db["records"]
users_collection = db["users"]