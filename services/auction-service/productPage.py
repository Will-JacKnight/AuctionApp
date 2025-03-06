from flask import Flask, request, jsonify, Blueprint
from supabaseClient import supabase
import os
import datetime
import uuid
from dotenv import load_dotenv
from flask_cors import CORS
import traceback
from collections import defaultdict
import threading
from flask_socketio import SocketIO, emit
import time
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys
import threading

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

RUN_MODE = os.getenv("RUN_MODE", "local")  # Default to local if not set
AZURE_BID_EMAIL_FUNCTION = os.getenv("AZURE_BID_EMAIL_FUNCTION")

if RUN_MODE == "docker":
    API_GATEWAY_URL = os.getenv("API_GATEWAY_DOCKER_URL")
elif RUN_MODE == "heroku":
    API_GATEWAY_URL = os.getenv("API_GATEWAY_HEROKU_URL")
else:  # Default to local
    API_GATEWAY_URL = os.getenv("API_GATEWAY_LOCAL_URL")

productPage = Blueprint("productPage", __name__)

current_auction_id = None # Track the auction ID being monitoreda
socketio = SocketIO() # Initialize the Websocket server
latest_max_bid = None  # Store last highest bid
polling_thread_started = False # Ensure to fetch data first before pulling bids

# Get the proudction information
@productPage.route('/product/<auction_id>', methods=['GET'])
def get_product_by_id(auction_id):
    global current_auction_id, polling_thread_started, latest_max_bid
    current_auction_id = auction_id # Assign the current auction id
    print(f"📩 Received request for auction_id: {auction_id}")

    if not auction_id:
        return jsonify({'error': 'auction_id is required'}), 400

    try:
        response = supabase.table('auctions').select(
            'name', 'description', 'status', 'start_date', 'start_time', 
            'starting_price', 'end_date', 'end_time', 'auction_type', 'image_url', 'seller_id'
        ).eq('id', auction_id).execute()

        if not response.data:
            print("⚠️ Auction not found for ID:", auction_id)
            return jsonify({"error": "Auction not found"}), 404
        
        item = response.data[0] # Get the first and only one item

        bid_response = (
            supabase.table('bids')
            .select('bid_amount')
            .eq('auction_id', auction_id)
            .order('bid_amount', desc=True)
            .limit(1)
            .execute()
        )
        max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None
        item["max_bid"] = max_bid # Add the max bidding price to the item

        itemList = []
        itemList.append(item)

        if not polling_thread_started:
            polling_thread_started = True
            threading.Thread(target=poll_for_new_bids, daemon=True).start()

        return jsonify(itemList), 200
    except Exception as e:
        print(f"🔥 Error retrieving auction: {e}")
        return jsonify({'error': str(e)}), 500

# Place the bid
@productPage.route('/place_bid', methods=['POST'])
@jwt_required()
def place_bid():
    user_id = get_jwt_identity()
    # Get the auctionId and bidPrice from frontend
    data = request.json
    print("Received bid request:", data)

    bid_price = data.get('bidPrice')
    auction_id = data.get('auctionId')

    print("current_auction_id is:", auction_id) # debug

    if bid_price is None:
        return jsonify({'error': 'bidPrice are required'}), 400

    try:
        new_bid = {
            'user_id': user_id, 
            'auction_id': auction_id,
            'bid_amount': bid_price,
            'created_at': datetime.datetime.utcnow().isoformat() 
        }

        # Insert the new bid into supabase
        response = supabase.table('bids').insert(new_bid).execute()

        # Emit WebSocket (in API gateway) event when a new bid is placed
        requests.post(f"{API_GATEWAY_URL}/bid_update", json={
            "auction_id": auction_id,
            "max_bid": bid_price
        })

        # call the notify function with the product id (asynchronously using threading)
        # notifyUsers("Iphone 16", bid_price, auction_id)
        email_thread = threading.Thread(target=notifyUsers, args=(bid_price, auction_id, user_id))
        email_thread.start()

        # Return the response to the frontend
        return jsonify({'message': 'Bid placed successfully', 'bid': response.data}), 201
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Polling new bids by Websocket
def poll_for_new_bids():
    global current_auction_id, latest_max_bid
    while True:
        if not current_auction_id:
            time.sleep(1)
            continue  # Skip iteration if no auction is set

        try:
            # Get the latest highest bid
            bid_response = (
                supabase.table('bids')
                .select('bid_amount')
                .eq('auction_id', current_auction_id)
                .order('bid_amount', desc=True)
                .limit(1)
                .execute()
            )
            new_max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None

            # Only send update if bid amount has changed
            if new_max_bid != latest_max_bid:
                latest_max_bid = new_max_bid

                # socketio.emit('bid_update', {'auction_id': current_auction_id, 'max_bid': new_max_bid})
                # Emit the bid update to the API Gateway
                requests.post(f"{API_GATEWAY_URL}/bid_update", json={
                        "auction_id": current_auction_id,
                        "max_bid": new_max_bid
                })

        except Exception as e:
            print("Error polling bids:", e)

        time.sleep(2)  # Wait 5 seconds before checking again


def notifyUsers(product_price, auction_id, user_id):
    
    print(f"auction_id: {auction_id} (type: {type(auction_id)})")
    sys.stdout.flush()
    
    # supabase calling
    product_name_response = supabase.table('auctions').select('name').eq('id', auction_id).execute()

    if not product_name_response.data:
        print("Auction not found.")
    else:
        product_name = product_name_response.data[0]['name']

    emails_response = (
        supabase
        .table('bids')
        .select('user_id, users(email)')  # Assuming 'users' is the foreign key reference
        .eq('auction_id', auction_id)
        .execute()
    )

    if emails_response.data:
        emails = list({entry['users']['email'] for entry in emails_response.data})  # Extract unique emails
        print("List of Emails:", emails)
    else:
        print("No bidders found.")

    bidder_email_response = (
        supabase
        .table('users')
        .select('email')  # Assuming 'users' is the foreign key reference
        .eq('id', user_id)
        .execute()
    )

    if not bidder_email_response.data:
        print("bidder id not found.")
    else:
        bidder_email = bidder_email_response.data[0]['email']

    # using emails 
    
    if bidder_email in emails:
        emails.remove(bidder_email)

    payload = {
        "emails": emails,
        "item": product_name,
        "bid": product_price    
    }

    try:
        # Send request to Azure Function
        response = requests.post(AZURE_BID_EMAIL_FUNCTION, json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        print("Sent all emails successfully")
        sys.stdout.flush()

    except requests.exceptions.RequestException as e:
        print("Exception occured when sending emails: ", str(e))
        sys.stdout.flush()



