from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from mongo_config import users_collection

auth_routes_bp = Blueprint('auth_routes', __name__)

@auth_routes_bp.route('/api/login', methods=['POST'])
def login():
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
