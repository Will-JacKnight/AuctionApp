import eventlet
# Enable eventlet for async operations
eventlet.monkey_patch()

import requests
import sys
import os
import logging
from dotenv import load_dotenv
from supabase import create_client
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Determine Microservices URLs based on environment mode
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
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize SocketIO with eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", logger=True, engineio_logger=True)

###############################
#       API ROUTES           #
###############################

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
        headers = {
        "Authorization": request.headers.get("Authorization")  
        }

        response = requests.post(f"{AUCTION_SERVICE_URL}/listing", files=files, data=form_data, headers=headers)
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

@app.route('/search_byTag', methods=['POST'])
def serach_byTag():
    """ Forward login request to User Service """
    response = requests.post(f"{AUCTION_SERVICE_URL}/search_byTag", json=request.json)
    return jsonify(response.json()), response.status_code


@app.route('/product/<auction_id>', methods=['GET'])
def bidding(auction_id):
    response = requests.get(f"{AUCTION_SERVICE_URL}/product/{auction_id}")
    return jsonify(response.json()), response.status_code

@app.route('/place_bid', methods=['POST'])
def place_bid():
    headers = {
        "Authorization": request.headers.get("Authorization"),  # Forward the token
        "Content-Type": request.headers.get("Content-Type", "application/json"),  # Forward Content-Type
    }
    response = requests.post(f"{AUCTION_SERVICE_URL}/place_bid", json=request.json, headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/dashboard_sell', methods=['GET'])
def sell():
    print("Received request at API Gateway")
    print("Gateway Headers:", dict(request.headers))  # Debugging
    sys.stdout.flush()

    headers = {
        "Authorization": request.headers.get("Authorization"),  # Forward the token
        "Content-Type": request.headers.get("Content-Type", "application/json"),  # Forward Content-Type
    }
    response = requests.get(f"{AUCTION_SERVICE_URL}/dashboard_sell", headers=headers)
    return jsonify(response.json()), response.status_code


@app.route('/dashboard_bid', methods=['GET'])
def bid():
    headers = {
        "Authorization": request.headers.get("Authorization"),  # Forward the token
        "Content-Type": request.headers.get("Content-Type", "application/json"),  # Forward Content-Type
    }

    response = requests.get(f"{AUCTION_SERVICE_URL}/dashboard_bid", headers=headers)
    return jsonify(response.json()), response.status_code

###############################
#   WebSocket Handlers       #
###############################

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
    port = int(os.environ.get("PORT", 4000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False, allow_unsafe_werkzeug=True)