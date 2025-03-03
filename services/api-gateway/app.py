import eventlet
eventlet.monkey_patch()
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv
from supabase import create_client
import logging
from flask_socketio import SocketIO, emit

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)

# Microservices URLs
# USER_SERVICE_URL = "http://user-service:8080"
# AUCTION_SERVICE_URL = "http://auction-service:7070"

MODE = os.getenv("RUN_MODE")
if MODE == "docker":
    AUCTION_SERVICE_URL = os.getenv("AUCTION_SERVICE_DOCKER_URL")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_DOCKER_URL")
elif MODE == "heroku":
    AUCTION_SERVICE_URL = os.getenv("AUCTION_SERVICE_HEROKU_URL")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_HEROKU_URL")
else:
    AUCTION_SERVICE_URL = os.getenv("AUCTION_SERVICE_LOCAL_URL")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_LOCAL_URL")
 

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
print(SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", logger=True, engineio_logger=True)


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


@app.route('/product/<auction_id>', methods=['GET'])
def bidding(auction_id):
    response = requests.get(f"{AUCTION_SERVICE_URL}/product/{auction_id}")
    return jsonify(response.json()), response.status_code

@app.route('/place_bid', methods=['POST'])
def place_bid():
    response = requests.post(f"{AUCTION_SERVICE_URL}/place_bid", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/dashboard_sell', methods=['GET'])
def sell():

    response = requests.get(f"{AUCTION_SERVICE_URL}/dashboard_sell")
    return jsonify(response.json()), response.status_code


@app.route('/dashboard_bid', methods=['GET'])
def bid():

    response = requests.get(f"{AUCTION_SERVICE_URL}/dashboard_bid")
    return jsonify(response.json()), response.status_code

# HTTP route to handle bid updates from the backend
@app.route('/bid_update', methods=['POST'])
def handle_bid_update_request():
    try:
        
        print(f"Received bid update request:", request.headers)
        print("Received request data:", request.data)

        # Ensure the request contains JSON data
        if not request.is_json:
            print("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.json
        print(f"Received bid update request: {data}")
         # Validate required fields
        if not data or "auction_id" not in data or "max_bid" not in data:
            print("Invalid data format")
            return jsonify({"error": "Invalid data format"}), 400
        

        # Forward the bid update to WebSocket clients
        socketio.emit('bid_update', data, to=None)
        return jsonify({"message": "Bid update forwarded"}), 200
    except Exception as e:
        print(f"Error handling bid update request: {e}")
        return jsonify({"error": str(e)}), 500
    
@socketio.on("connect")
def handle_connect():
    print("Client connected to WebSocket")
    emit("connection_success", {"message": "WebSocket connected"})

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected from WebSocket")

@socketio.on("bid_update")
def handle_bid_update(data):
    print(f"Received bid update from Auction Service: {data}")
    # Broadcast the bid update to all connected clients
    emit("bid_update", data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=4000, debug=True, allow_unsafe_werkzeug=True)