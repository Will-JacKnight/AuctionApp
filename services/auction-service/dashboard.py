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
 
 
 
# # Load environment variables
# dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
# load_dotenv(dotenv_path)
 
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
        # Raw SQL function definition in Supabase SQL Function Editor
        """
        CREATE OR REPLACE FUNCTION getting_seller_auction(seller_id_param UUID)
        RETURNS TABLE (
            id UUID,  -- Changed from auction_id to id
            name TEXT,
            description TEXT,
            image_url TEXT,
            status TEXT,
            starting_price NUMERIC,
            max_bid NUMERIC
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                a.id,  -- Ensure this matches the expected "id"
                a.name,
                a.description,
                a.image_url,
                a.status,
                a.starting_price,
                (SELECT MAX(b.bid_amount) FROM bids b WHERE b.auction_id = a.id) AS max_bid
            FROM auctions a
            WHERE a.seller_id = seller_id_param;
        END;
        $$ LANGUAGE plpgsql;
        """

        # Get seller's username
        username_response = supabase.table('users').select('username').eq('id', seller_id).execute()
        username = username_response.data

        if not username:
            return jsonify({'error': 'Seller not found'}), 404

        # Use `rpc()` to call the SQL function stored in Supabase
        items_response = supabase.rpc("getting_seller_auction", {"seller_id_param": seller_id}).execute()
        items = items_response.data if items_response.data else []
        print(items)

        if not items:
            return jsonify({'message': 'No items found for this seller'}), 200
        items_list = []
        for item in items:
            items_list.append(item)
        return jsonify(items_list), 200

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
            product_id UUID
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                a.name AS auction_name,
                b.bid_amount,
                b.created_at::TIMESTAMP WITHOUT TIME ZONE,
                a.status,
                (SELECT MAX(b2.bid_amount) FROM bids b2 WHERE b2.auction_id = b.auction_id) AS max_bid
                a.id
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
                "max_bid": bid["max_bid"],
                "product_id": bid["product_id"]
            })

        return jsonify([{name: history} for name, history in auction_bids.items()]), 200

    except Exception as e:
        print("Error:", e, flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


 
# if __name__ == "__main__":
#     app.run(debug=True)