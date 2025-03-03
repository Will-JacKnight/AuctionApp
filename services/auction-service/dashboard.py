from flask import Flask, request, jsonify, Blueprint
from supabase import create_client, Client
import os
import datetime
import uuid
from dotenv import load_dotenv
from flask_cors import CORS
import traceback
from collections import defaultdict

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
def dashboard_sell():
    # data = request.json
    # seller_id = data.get('seller_id')
    seller_id = "b7f65d95-7589-4dca-a389-5e293bd648e4"
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
        .select('bid_amount, created_at, auctions(name, status)')  # Implicit join
        .eq('user_id', seller_id)
        .execute()
        )
        bids = bids_response.data
        
        if not bids:
            return jsonify({'message': 'No bids found for this user'}), 200
        
        auction_bids = defaultdict(list)

        for bid in bids:
            auction_name = bid['auctions']['name']
            auction_bids[auction_name].append({
                "bid_amount": bid["bid_amount"],
                "created_at": bid["created_at"],
                "status": bid["auctions"]["status"],
                "item_name": bid['auctions']['name']
            })
        bids_list = [{name: history} for name, history in auction_bids.items()]
        print(bids_list, flush=True)

        return jsonify(bids_list), 200

    except Exception as e:
        print("Error:", e, flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500 

# if __name__ == "__main__":
#     app.run(debug=True)