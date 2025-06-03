# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from mongo_config import users_collections

auth_routes_bp = Blueprint('auth_routes', __name__)

def handle_login(site):
    users_collection = users_collections.get(site)
    if users_collection is None:
        return jsonify({'error': 'Invalid site'}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = users_collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        token = create_access_token(identity=username)
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@auth_routes_bp.route('/api/drdo_portal/login', methods=['POST'])
def login_portal():
    return handle_login("drdo_portal")


@auth_routes_bp.route('/api/drdoone/login', methods=['POST'])
def login_one():
    return handle_login("drdoone")


@auth_routes_bp.route('/api/drdotwo/login', methods=['POST'])
def login_two():
    return handle_login("drdotwo")
