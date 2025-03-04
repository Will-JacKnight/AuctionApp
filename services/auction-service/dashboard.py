from flask import Flask, request, jsonify, Blueprint
from supabase import create_client, Client
import os
import datetime
import uuid
from dotenv import load_dotenv
from flask_cors import CORS
import traceback
from collections import defaultdict
import logging
import sys
from flask_jwt_extended import jwt_required, get_jwt_identity



# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

dashboard = Blueprint("dashboard", __name__)

# Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# app = Flask(__name__)
# CORS(app)

@dashboard.route('/dashboard_sell', methods=['GET'])
@jwt_required()
def dashboard_sell():
    print("Request received at /dashboard_sell")
    sys.stdout.flush()  # Ensures logs are immediately written

    # Print all request headers
    print("Request Headers:", dict(request.headers))
    sys.stdout.flush()

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    print("Received JWT:", f"'{token}'")  # Add quotes to detect if it's an empty string

    seller_id = get_jwt_identity()  # Extract user data from JWT
    # print("printing the user ", user)
    # sys.stdout.flush()
    # # user_id = user.get("id")  # Get the user ID from the token
    # print("User ID from JWT:", user_id)
    # sys.stdout.flush()

    # data = request.json
    # seller_id = data.get('seller_id')
    # seller_id = "b7f65d95-7589-4dca-a389-5e293bd648e4"
    if not seller_id:
        return jsonify({'error': 'seller_id is required'}), 400

    try:
        # get the username
        username_response = supabase.table('users').select('username').eq('id', seller_id).execute()
        username = username_response.data  

        # If no user is found, return a 404 response
        if not username:
            return jsonify({'error': 'Seller not found'}), 404

        # get the selling items
        items_response = supabase.table('auctions').select('id', 'name', 'description', 'image_url', 'status').eq('seller_id', seller_id).execute()
        items = items_response.data

        if not items:
            return jsonify({'message': 'No items found for this seller'}), 200

        bids = {}
        for item in items:
            auction_id = item['id']
            bid_response = (
                supabase.table('bids')
                .select('bid_amount')
                .eq('auction_id', auction_id)
                .order('bid_amount', desc=True)  # Sort by bid_amount in descending order
                .limit(1)  # Get the highest bid
                .execute()
            )
            max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None
            bids[auction_id] = max_bid  # Store max bid for each auction

        # Combine items with their max bid amount
        for item in items:
            item['max_bid'] = bids.get(item['id'], None)
            

        return jsonify({'username': username, 'items': items}), 200
    except Exception as e:
        print("Error:", e, flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@dashboard.route('/dashboard_bid', methods=['GET'])
def dashboard_bid():
    # data = request.json
    # seller_id = data.get('seller_id')
    seller_id = "b7f65d95-7589-4dca-a389-5e293bd648e4"

    # if not seller_id:
    #     return jsonify({'error': 'seller_id is required'}), 400

    try:
        # get the username
        username_response = supabase.table('users').select('username').eq('id', seller_id).execute()
        username = username_response.data

        if not username:
            return jsonify({'error': 'User not found'}), 404

        # get the bidding items
        bids_response = (
        supabase.table('bids')
        .select('bid_amount, created_at, auction_id, auctions(name, status)')  # Implicit join
        .eq('user_id', seller_id)
        .execute()
        )
        bids = bids_response.data
        
        if not bids:
            return jsonify({'message': 'No bids found for this user'}), 200
        
        auction_bids = defaultdict(list)

        for bid in bids:
            auction_id = bid['auction_id']
            # Fetch the max_bid for this auction
            max_bid_response = (
                supabase.table('bids')
                .select('bid_amount')
                .eq('auction_id', auction_id)
                .order('bid_amount', desc=True)  # Sort in descending order
                .limit(1)  # Get the highest bid
                .execute()
            )

            # Get the highest bid amount (if exists)
            max_bid = max_bid_response.data[0]['bid_amount'] if max_bid_response.data else None

            auction_name = bid['auctions']['name']
            auction_bids[auction_name].append({
                "bid_amount": bid["bid_amount"],
                "created_at": bid["created_at"],
                "status": bid["auctions"]["status"],
                "item_name": bid['auctions']['name'],
                "max_bid": max_bid
            })
        bids_list = [{name: history} for name, history in auction_bids.items()]
        # print(bids_list, flush=True)

        return jsonify(bids_list), 200

    except Exception as e:
        print("Error:", e, flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500 

# if __name__ == "__main__":
#     app.run(debug=True)