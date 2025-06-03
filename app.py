from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from routes.auth_routes import auth_routes_bp
from routes.data_entry import create_data_entry_blueprint
from routes.dashboard import dashboard_bp

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

# Auth routes with site-specific login URLs
app.register_blueprint(auth_routes_bp)

# Data entry routes for each site with URL prefixes
app.register_blueprint(create_data_entry_blueprint("drdo_portal"), url_prefix='/api/form/drdo_portal')
app.register_blueprint(create_data_entry_blueprint("drdoone"), url_prefix='/api/form/drdoone')
app.register_blueprint(create_data_entry_blueprint("drdotwo"), url_prefix='/api/form/drdotwo')

# Dashboard routes for each site with URL prefixes
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

@app.route('/')
def home():
    return "Backend server running"

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
