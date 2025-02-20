from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
import datetime
import uuid
from dotenv import load_dotenv
from flask_cors import CORS
import traceback

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "product_images"

@app.route('/listing', methods=['POST'])
def create_item():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        name = data.get('name')
        category = data.get('category')
        description = data.get('description')
        starting_price = data.get('starting_price')
        start_date = data.get('start_date')  # e.g. "2025-05-01"
        start_time = data.get('start_time')  # e.g. "09:00"
        end_date = data.get('end_date')
        end_time = data.get('end_time')
        image_url = data.get("image_url", "")

        if not all([name, category, description, starting_price, start_date, start_time, end_date, end_time]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            starting_price = float(starting_price)
        except ValueError:
            return jsonify({"error": "Invalid starting price"}), 400

        current_time = datetime.datetime.utcnow()

        try:
            start_dt_str = f"{start_date} {start_time}"  # "2025-05-01 09:00"
            end_dt_str = f"{end_date} {end_time}"        # "2025-05-02 10:00"
            start_dt = datetime.datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M")
            end_dt = datetime.datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({"error": "Invalid date/time format. Use YYYY-MM-DD for date and HH:MM for time."}), 400

        if start_dt <= current_time:
            return jsonify({"error": "Start time must be in the future"}), 400
        if start_dt >= end_dt:
            return jsonify({"error": "Start time must be before end time"}), 400

        new_item = supabase.table("auctions").insert({
            "item_name": name,
            "category": category,
            "description": description,
            "starting_price": starting_price,
            "start_date": start_date,
            "start_time": start_dt.strftime('%H:%M'),
            "end_date": end_date,
            "end_time": end_dt.strftime('%H:%M'),
            "auction_type": "English",
            "image_url": image_url,
            "created_at": datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }).execute()

        return jsonify({
            "message": "New item created",
            "item_id": new_item.data[0]["id"] if new_item.data else None,
            "image_url": image_url
        }), 201

    except Exception as e:
        traceback.print_exc()
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070, debug=True)
