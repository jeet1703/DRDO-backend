from flask import Blueprint, jsonify, request
from mongo_config import records_collections
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint('dashboard', __name__)

def get_collection(site):
    return records_collections.get(site)

# [Keep all existing GET endpoints exactly as they were originally]
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

# [New dedicated comment endpoint]
@dashboard_bp.route('/<site>/comment/<string:reference_no>', methods=['POST'])
@jwt_required()
def add_comment(site, reference_no):
    data = request.json
    if not data or 'comment' not in data:
        return jsonify({"error": "Comment text required"}), 400

    records_collection = get_collection(site)
    if not records_collection:
        return jsonify({"error": "Invalid site"}), 400

    comment_obj = {
        "text": data['comment'],
        "timestamp": datetime.utcnow().isoformat(),
        "user": get_jwt_identity() or "unknown"
    }

    result = records_collection.update_one(
        {"referenceNo": reference_no},
        {"$push": {"comments": comment_obj}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Comment added successfully"}), 200

# [Keep original PUT endpoints exactly as they were]
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

# [Similarly keep drdoone and drdotwo update endpoints unchanged]