from flask import Flask
from mainPage import mainPage  # Import the Blueprint
# from .app_create_project import create_bp
# from .app_manage_project import manage_bp
# from .app_profile import profile_bp
# from .app_search_project import search_bp
# from database.connection import close_db

# Create an instance of the Flask class for the web application
app = Flask(__name__)

# Register blueprints to modularize the application
# Each blueprint corresponds to a specific set of routes and functionality
# Register the Blueprint for mainPage
app.register_blueprint(mainPage)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)