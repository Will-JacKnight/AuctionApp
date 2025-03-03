import os

from flask import Flask
from mainPage import mainPage  # Import the Blueprint
from listingPage import listingPage
from dashboard import dashboard
from flask_cors import CORS
from productPage import productPage, socketio
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

# from .app_create_project import create_bp
# from .app_manage_project import manage_bp
# from .app_profile import profile_bp
# from .app_search_project import search_bp
# from database.connection import close_db

# Create an instance of the Flask class for the web application
app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*") 

# Register blueprints to modularize the application
# Each blueprint corresponds to a specific set of routes and functionality
# Register the Blueprint for mainPage
app.register_blueprint(mainPage)
app.register_blueprint(listingPage)
app.register_blueprint(dashboard)
app.register_blueprint(productPage)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7070))
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
