# File: backend/routes/dashboard.py
from flask import Blueprint, jsonify
from mongo_config import records_collection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def get_records():
    records = list(records_collection.find({}, {'_id': 0}))
    return jsonify(records)
