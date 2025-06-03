from flask import Blueprint, jsonify, request
from mongo_config import records_collections

dashboard_bp = Blueprint('dashboard', __name__)

def get_collection(site):
    return records_collections.get(site)

@dashboard_bp.route('/drdo_portal/', methods=['GET'])
def get_records_portal():
    records_collection = get_collection("drdo_portal")
    records = list(records_collection.find({}, {'_id': 0}))
    for idx, record in enumerate(records):
        record["id"] = idx + 1
    return jsonify(records)

@dashboard_bp.route('/drdoone/', methods=['GET'])
def get_records_one():
    records_collection = get_collection("drdoone")
    records = list(records_collection.find({}, {'_id': 0}))
    for idx, record in enumerate(records):
        record["id"] = idx + 1
    return jsonify(records)

@dashboard_bp.route('/drdotwo/', methods=['GET'])
def get_records_two():
    records_collection = get_collection("drdotwo")
    records = list(records_collection.find({}, {'_id': 0}))
    for idx, record in enumerate(records):
        record["id"] = idx + 1
    return jsonify(records)


@dashboard_bp.route('/drdo_portal/update/<string:reference_no>', methods=['PUT'])
def update_record_portal(reference_no):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    records_collection = get_collection("drdo_portal")
    result = records_collection.update_one(
        {"referenceNo": reference_no},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Record updated successfully"}), 200

@dashboard_bp.route('/drdoone/update/<string:reference_no>', methods=['PUT'])
def update_record_one(reference_no):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    records_collection = get_collection("drdoone")
    result = records_collection.update_one(
        {"referenceNo": reference_no},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Record updated successfully"}), 200

@dashboard_bp.route('/drdotwo/update/<string:reference_no>', methods=['PUT'])
def update_record_two(reference_no):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    records_collection = get_collection("drdotwo")
    result = records_collection.update_one(
        {"referenceNo": reference_no},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Record updated successfully"}), 200
