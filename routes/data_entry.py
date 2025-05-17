# File: backend/routes/data_entry.py
from flask import Blueprint, request, jsonify
from mongo_config import records_collection

data_entry_bp = Blueprint('data_entry', __name__)

#@data_entry_bp.route('/', methods=['POST'])
#def submit_data():
#    data = request.json
#    records_collection.insert_one(data)
#    return jsonify({"message": "Record added successfully"}), 201

@data_entry_bp.route('/records', methods=['POST'])  # Change here
def submit_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print("Received data:", data)  # ✅ Print to terminal/log
    records_collection.insert_one(data)
    return jsonify({"message": "Record added successfully"}), 201
