import eventlet
# Enable eventlet for async operations
eventlet.monkey_patch()

import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_jwt_extended import JWTManager

# Import Blueprints for modular route management
from mainPage import mainPage
from listingPage import listingPage
from dashboard import dashboard
from productPage import productPage, socketio

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configure JWT Authentication
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Initialize WebSocket support
socketio.init_app(app, cors_allowed_origins="*")

# Register Blueprints to modularize the application
app.register_blueprint(mainPage)
app.register_blueprint(listingPage)
app.register_blueprint(dashboard)
app.register_blueprint(productPage)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7070))
    app.run(host='0.0.0.0', port=port, debug=True)
