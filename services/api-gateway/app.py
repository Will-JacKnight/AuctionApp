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
load_dotenv()

app = Flask(__name__)
CORS(app)

# Microservices URLs
USER_SERVICE_URL = "http://user-service:8080"
AUCTION_SERVICE_URL = "http://auction-service:7070"

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
print(SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # Storage Bucket Name
# BUCKET_NAME = "product_images"

# # Configure Upload Folder
# UPLOAD_FOLDER = "uploads"
# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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
        data = request.json
        logging.debug(f"🔍 Received data: {data}") 

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        
        if "starting_price" not in data or data["starting_price"] is None:
            return jsonify({"error": "Missing required field: starting_price"}), 400

        result = supabase.table("auctions").insert(data).execute()
        logging.debug(f"📌 Supabase Response: {result}")

        return jsonify({"message": "Auction created successfully"}), 201
    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "gif"}

# @app.route('/listing', methods=['POST'])
# def listing():
#     """ Handle auction upload and forward request to Auction Service """
#     if "productImage" not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files["productImage"]
#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     if file and allowed_file(file.filename):
#         # Generate a secure file name
#         file_extension = file.filename.rsplit(".", 1)[1].lower()
#         file_name = f"{uuid.uuid4()}.{file_extension}"
        
#         # Upload image to Supabase Storage
#         response = supabase.storage.from_(BUCKET_NAME).upload(file_name, file.stream, content_type=f"image/{file_extension}")
        
#         if "error" in response:
#             return jsonify({"error": response["error"]["message"]}), 500

#         # Retrieve the public access `image_url` from Supabase
#         image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_name}"

#         # Retrieve form data and add Supabase `image_url`
#         data = {key: request.form[key] for key in request.form}
#         data["image_url"] = image_url
        
#         # Insert into `auctions` table
#         new_item = supabase.table("auctions").insert(data).execute()

#         response = requests.post(f"{AUCTION_SERVICE_URL}/upload-auction", json=data)
#         return jsonify(response.json()), response.status_code
        
#     return jsonify({"error": "Invalid file type"}), 400


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)