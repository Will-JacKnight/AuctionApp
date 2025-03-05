from flask import Flask, request, jsonify, Blueprint
from supabaseClient import supabase
import os
import datetime
import uuid
from dotenv import load_dotenv
from flask_cors import CORS
import traceback
from flask_jwt_extended import jwt_required, get_jwt_identity


# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

listingPage = Blueprint("listingPage", __name__)

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")

BUCKET_NAME = "product_images"

# Allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    """ Check if file extension is allowed """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@listingPage.route('/listing', methods=['POST'])
@jwt_required()
def create_item():
    seller_id = get_jwt_identity()
    try:
        # Extract form-data fields
        data = {key: request.form[key] for key in request.form}
        image_url = None

        # Validate required fields
        required_fields = ["name", "category", "description", "starting_price", "start_date", "start_time", "end_date", "end_time"]
        if not all(field in data and data[field].strip() for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            data["starting_price"] = float(data["starting_price"])
        except ValueError:
            return jsonify({"error": "Invalid starting price"}), 400
        
        # Validate date & time format
        current_time = datetime.datetime.utcnow()
        try:
            start_dt_str = f"{data['start_date']} {data['start_time']}"  # "2025-05-01 09:00"
            end_dt_str = f"{data['end_date']} {data['end_time']}"        # "2025-05-02 10:00"
            start_dt = datetime.datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M")
            end_dt = datetime.datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid date/time format. Use YYYY-MM-DD for date and HH:MM for time."}), 400
        
        if start_dt <= current_time:
            return jsonify({"error": "Start time must be in the future"}), 400
        if start_dt >= end_dt:
            return jsonify({"error": "Start time must be before end time"}), 400
        
        # Handle image upload if present
        if "productImage" in request.files:
            file = request.files["productImage"]
            if file and allowed_file(file.filename):
                file_extension = file.filename.rsplit(".", 1)[1].lower()
                file_name = f"{uuid.uuid4()}.{file_extension}" # Assign the file name randomly

                # Read file as bytes
                file_bytes = file.read()

                # Upload to Supabase Storage (using bytes data)
                response = supabase.storage.from_(BUCKET_NAME).upload(file_name, file_bytes)

                # Ensure upload was successful
                if not response:
                    return jsonify({"error": "Failed to upload image to Supabase"}), 500

                # Construct public URL
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_name}"
                data["image_url"] = image_url

        # Insert into `auctions` table
        new_item = supabase.table("auctions").insert({
            "name": data["name"],
            "seller_id": seller_id,
            "category": data["category"],
            "description": data["description"],
            "starting_price": data["starting_price"],
            "start_date": data["start_date"],
            "start_time": start_dt.strftime('%H:%M'),
            "end_date": data["end_date"],
            "end_time": end_dt.strftime('%H:%M'),
            "auction_type": "English",
            "status": 'active',
            "image_url": image_url,  # Store the image URL
            "created_at": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }).execute()

        return jsonify({
            "message": "New item created",
            "item_id": new_item.data[0]["id"] if new_item.data else None,
            "image_url": image_url
        }), 201
 
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
