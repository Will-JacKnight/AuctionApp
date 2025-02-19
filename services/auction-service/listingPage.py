from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
import datetime
import uuid
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Storage Bucket Name
BUCKET_NAME = "product_images"

### ** Create Item with Image Upload**
@app.route('/item', methods=['POST'])
def create_item():
    try:
        # Handle both form-data (file) and JSON data
        data = request.json
        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        starting_price = data.get('starting_price')
        start_date = data.get('start_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        image_url = data.get("image_url")  # Get image file from request

        # Validate required fields
        if not all([name, category, description, starting_price, start_time, end_time, image_file]):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert starting price to float
        try:
            starting_price = float(starting_price)
        except ValueError:
            return jsonify({"error": "Invalid starting price"}), 400

        # Get the current time in UTC
        current_time = datetime.datetime.utcnow()

        # Validate date format and ensure `start_time` is in the future
        try:
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
        except ValueError:
            return jsonify({"error": "Invalid date format, use ISO format (YYYY-MM-DD HH:MM:SS)"}), 400

        # Ensure start_time is in the future
        if start_time <= current_time:
            return jsonify({"error": "Start time must be in the future"}), 400


        # Ensure start time is before end time
        if start_time >= end_time:
            return jsonify({"error": "Start time must be before end time"}), 400

        # # Upload image to Supabase Storage
        # file_extension = image_file.filename.split('.')[-1]
        # file_name = f"{uuid.uuid4()}.{file_extension}"  # Generate unique filename
        # response = supabase.storage.from_(BUCKET_NAME).upload(file_name, image_file.stream, content_type=f"image/{file_extension}")

        # if "error" in response:
        #     return jsonify({"error": response["error"]["message"]}), 500

        # # Generate public URL for the image
        # image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_name}"

        # Insert into database
        new_item = supabase.table("auctions").insert({
            "item_name": name,
            "category": category,
            "description": description,
            "starting_price": starting_price,
            'start_date': start_date,
            "start_time": start_time.strftime('%H:%M'),
            "end_time": end_time.strftime('%H:%M'),
            "auction_type": "English",
            "image_url": image_url,  # Store image URL in the database
            "created_at": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }).execute()

        return jsonify({"message": "New item created", "item_id": new_item.data[0]["id"], "image_url": image_url}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070, debug=True)