from flask import Blueprint, request, jsonify
import hashlib

auth_routes_bp = Blueprint('auth_routes', __name__)

# fake data
users = {
    "admin": hashlib.sha256("password123".encode()).hexdigest()
}

@auth_routes_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if users.get(email) == hashed_pw:
        return jsonify({'message': 'Login successful', 'token': 'fake-jwt-token'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401
