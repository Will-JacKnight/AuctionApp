from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Microservices URLs
USER_SERVICE_URL = "http://user-service:8080"
AUCTION_SERVICE_URL = "http://auction-service:7070"

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Storage Bucket Name
BUCKET_NAME = "product_images"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"png", "jpg", "jpeg", "gif"}

@app.route('/listing', methods=['POST'])
def listing():
    """ Handle auction upload and forward request to Auction Service """
    if "productImage" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["productImage"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Generate a secure file name
        file_extension = file.filename.rsplit(".", 1)[1].lower()
        file_name = f"{uuid.uuid4()}.{file_extension}"
        
        # Upload image to Supabase Storage
        response = supabase.storage.from_(BUCKET_NAME).upload(file_name, file.stream, content_type=f"image/{file_extension}")
        
        if "error" in response:
            return jsonify({"error": response["error"]["message"]}), 500

        # Retrieve the public access `image_url` from Supabase
        image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_name}"

        # Retrieve form data and add Supabase `image_url`
        data = {key: request.form[key] for key in request.form}
        data["image_url"] = image_url
        
        # Insert into `auctions` table
        new_item = supabase.table("auctions").insert(data).execute()
        
        return jsonify({"message": "Auction created successfully", "item_id": new_item.data[0]["id"], "image_url": image_url}), 201

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
