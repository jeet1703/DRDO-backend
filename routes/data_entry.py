# File: backend/routes/data_entry.py
from flask import Blueprint, request, jsonify
from mongo_config import records_collection

data_entry_bp = Blueprint('data_entry', __name__)

@data_entry_bp.route('/', methods=['POST'])
def submit_data():
    data = request.json
    records_collection.insert_one(data)
    return jsonify({"message": "Record added successfully"}), 201