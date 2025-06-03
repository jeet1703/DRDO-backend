# mongo_config.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Static databases
db_drdo_portal = client["drdo_portal"]
db_drdoone = client["drdoone"]
db_drdotwo = client["drdotwo"]

# Collections
records_collections = {
    "drdo_portal": db_drdo_portal["records"],
    "drdoone": db_drdoone["records"],
    "drdotwo": db_drdotwo["records"]
}

users_collections = {
    "drdo_portal": db_drdo_portal["users"],
    "drdoone": db_drdoone["users"],
    "drdotwo": db_drdotwo["users"]
}
