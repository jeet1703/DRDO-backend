# routes/data_entry.py
from flask import Blueprint, request, jsonify
from mongo_config import records_collections

def create_data_entry_blueprint(site_name):
    data_entry_bp = Blueprint(f'data_entry_{site_name}', __name__)

    @data_entry_bp.route('/records', methods=['POST'])
    def submit_data():
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        print(f"Received data for {site_name}:", data)
        records_collections[site_name].insert_one(data)
        return jsonify({"message": "Record added successfully"}), 201

    return data_entry_bp
