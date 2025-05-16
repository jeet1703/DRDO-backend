from flask import Flask, request
from routes.data_entry import data_entry_bp
from routes.dashboard import dashboard_bp
from routes.auth_routes import auth_routes_bp
from auth import require_auth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():#
    return "Backend server is running"#

@app.before_request
def check_auth():
    if request.path != '/api/login':
        require_auth()

# Register blueprints
app.register_blueprint(data_entry_bp, url_prefix='/api/form')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(auth_routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
