# File: backend/app.py
from flask import Flask
from routes.data_entry import data_entry_bp
from routes.dashboard import dashboard_bp
from auth import require_auth

app = Flask(__name__)

# Middleware for authentication (placeholder)
@app.before_request
def check_auth():
    require_auth()

# Register blueprints
app.register_blueprint(data_entry_bp, url_prefix='/api/form')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
