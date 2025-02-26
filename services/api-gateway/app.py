from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv
from supabase import create_client
import logging

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)

# Microservices URLs
USER_SERVICE_URL = "http://user-service:8080"
AUCTION_SERVICE_URL = "http://auction-service:7070"

MODE = os.getenv("RUN_MODE")
if MODE == "local":
    AUCTION_SERVICE_URL = "http://127.0.0.1:7070"
    USER_SERVICE_URL = "http://127.0.0.1:8080"

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
print(SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/signup', methods=['POST'])
def register():
    """ Forward registration request to User Service """
    response = requests.post(f"{USER_SERVICE_URL}/signup", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/login', methods=['POST'])
def login():
    """ Forward login request to User Service """
    response = requests.post(f"{USER_SERVICE_URL}/login", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/listing', methods=['POST'])
def listing():
    try:
        if "productImage" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["productImage"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        form_data = {key: request.form[key] for key in request.form}
 
        files = {"productImage": (file.filename, file.stream, file.content_type)}
 
        response = requests.post(f"{AUCTION_SERVICE_URL}/listing", files=files, data=form_data)
        return jsonify(response.json()), response.status_code
 
    except Exception as e:
        logging.error(f"Error forwarding request: {str(e)}")
        return jsonify({"error": str(e)}), 500
        
@app.route('/display_mainPage', methods=['GET'])
def display():
    """ Forward login request to User Service """
    response = requests.get(f"{AUCTION_SERVICE_URL}/display_mainPage")
    return jsonify(response.json()), response.status_code

@app.route('/search', methods=['POST'])
def serach():
    """ Forward login request to User Service """
    response = requests.post(f"{AUCTION_SERVICE_URL}/search", json=request.json)
    return jsonify(response.json()), response.status_code


@app.route('/product', methods=['GET'])
def display():

    response = requests.get(f"{AUCTION_SERVICE_URL}/product")
    return jsonify(response.json()), response.status_code


@app.route('/dashboard_sell', methods=['GET'])
def display():

    response = requests.get(f"{AUCTION_SERVICE_URL}/dashboard_sell")
    return jsonify(response.json()), response.status_code


@app.route('/dashboard_bid', methods=['GET'])
def display():

    response = requests.get(f"{AUCTION_SERVICE_URL}/dashboard_bid")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)