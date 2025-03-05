from flask import Flask, request, jsonify, Blueprint
from supabaseClient import supabase
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
 

# app = Flask(__name__)
# CORS(app)
 
@dashboard.route('/dashboard_sell', methods=['GET'])
@jwt_required()
def dashboard_sell():
    seller_id = get_jwt_identity()  # Extract user data from JWT
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
@jwt_required()
def dashboard_bid():
    seller_id = get_jwt_identity()
    if not seller_id:
        return jsonify({'error': 'seller_id is required'}), 400

    try:
        # Raw SQL in Supabase SQL Function Editor
        """
        CREATE OR REPLACE FUNCTION get_user_bids(user_id_param UUID)
        RETURNS TABLE (
            auction_name TEXT,
            bid_amount NUMERIC,
            created_at TIMESTAMP WITHOUT TIME ZONE,
            status TEXT,
            max_bid NUMERIC
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                a.name AS auction_name,
                b.bid_amount,
                b.created_at::TIMESTAMP WITHOUT TIME ZONE,
                a.status,
                (SELECT MAX(b2.bid_amount) FROM bids b2 WHERE b2.auction_id = b.auction_id) AS max_bid
            FROM bids b
            JOIN auctions a ON a.id = b.auction_id
            WHERE b.user_id = user_id_param;
        END;
        $$ LANGUAGE plpgsql;
        """

        # use `rpc()` to call the SQL function stored in Supabase
        bids_response = supabase.rpc("get_user_bids", {"user_id_param": seller_id}).execute()
        bids = bids_response.data

        if not bids:
            return jsonify({'message': 'No bids found for this user'}), 200

        # Formating output
        auction_bids = defaultdict(list)
        for bid in bids:
            auction_name = bid["auction_name"]
            auction_bids[auction_name].append({
                "bid_amount": bid["bid_amount"],
                "created_at": bid["created_at"],
                "status": bid["status"],
                "item_name": auction_name,
                "max_bid": bid["max_bid"]
            })

        return jsonify([{name: history} for name, history in auction_bids.items()]), 200

    except Exception as e:
        print("Error:", e, flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


 
# if __name__ == "__main__":
#     app.run(debug=True)