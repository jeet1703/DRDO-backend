# File: backend/routes/dashboard.py
from flask import Blueprint, jsonify, request
from mongo_config import records_collection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def get_records():
    records = list(records_collection.find({}, {'_id': 0}))
     # Add sequential `id` required by frontend
    for idx, record in enumerate(records):
        record["id"] = idx + 1
    return jsonify(records)



@dashboard_bp.route('/update/<string:reference_no>', methods=['PUT'])
def update_record(reference_no):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    result = records_collection.update_one(
        {"referenceNo": reference_no},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Record updated successfully"}), 200

