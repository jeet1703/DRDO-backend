from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from routes.auth_routes import auth_routes_bp
from routes.data_entry import data_entry_bp
from routes.dashboard import dashboard_bp

load_dotenv()

app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

app.register_blueprint(auth_routes_bp)
app.register_blueprint(data_entry_bp, url_prefix='/api/form')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

@app.route('/')
def home():
    return "Backend server running"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
