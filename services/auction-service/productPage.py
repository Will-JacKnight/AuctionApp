from flask import Flask, request, jsonify, Blueprint
from supabase import create_client, Client
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

# # Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")  # Adjust this path as needed
load_dotenv(dotenv_path)

RUN_MODE = os.getenv("RUN_MODE", "local")  # Default to local if not set

if RUN_MODE == "docker":
    API_GATEWAY_URL = os.getenv("API_GATEWAY_DOCKER_URL")
elif RUN_MODE == "heroku":
    API_GATEWAY_URL = os.getenv("API_GATEWAY_HEROKU_URL")
else:  # Default to local
    API_GATEWAY_URL = os.getenv("API_GATEWAY_LOCAL_URL")

productPage = Blueprint("productPage", __name__)

# # Supabase Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# app = Flask(__name__)
# CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets
socketio = SocketIO() 

current_auction_id = None 
latest_max_bid = None  # Store last highest bid
polling_thread_started = False

@productPage.route('/product/<auction_id>', methods=['GET'])
def get_product_by_id(auction_id):
    print(f"📩 Received request for auction_id: {auction_id}")

    if not auction_id:
        return jsonify({'error': 'auction_id is required'}), 400

    try:
        response = supabase.table('auctions').select(
            'name', 'description', 'status', 'start_date', 'start_time', 
            'starting_price', 'end_date', 'end_time', 'auction_type', 'image_url'
        ).eq('id', auction_id).execute()

        if not response.data:
            print("⚠️ Auction not found for ID:", auction_id)
            return jsonify({"error": "Auction not found"}), 404

        item = response.data[0]

        bid_response = (
            supabase.table('bids')
            .select('bid_amount')
            .eq('auction_id', auction_id)
            .order('bid_amount', desc=True)
            .limit(1)
            .execute()
        )
        max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None
        item["max_bid"] = max_bid 

        return jsonify(item), 200
    except Exception as e:
        print(f"🔥 Error retrieving auction: {e}")
        return jsonify({'error': str(e)}), 500



# @productPage.route('/product/<auction_id>', methods=['GET'])
# def get_product_by_id(auction_id):
#     print(f"Received request for auction_id: {auction_id}")

#     if not auction_id:
#         return jsonify({'error': 'auction_id is required'}), 400

#     try:
#         response = supabase.table('auctions').select(
#             'name', 'description', 'status', 'start_date', 'start_time', 
#             'starting_price', 'end_date', 'end_time', 'auction_type', 'image_url'
#         ).eq('id', auction_id).execute()

#         if not response.data:
#             print("⚠️ Auction not found for ID:", auction_id)
#             return jsonify({"error": "Auction not found"}), 404

#         item = response.data[0]
#         return jsonify(item), 200
#     except Exception as e:
#         print(f"🔥 Error retrieving auction: {e}")
#         return jsonify({'error': str(e)}), 500


# @productPage.route('/product', methods=['GET', 'POST'])
# def product():
#     data = request.get_json()
#     auction_id = data.get('auction_id')

#     global current_auction_id, latest_max_bid, polling_thread_started
#     # auction_id = "b3dd3d7f-1f20-4f79-9651-b33b9f411600"
#     current_auction_id = auction_id

#     if not auction_id:
#         return jsonify({'error': 'auction_id is required'}), 400
#     try:
#         response = supabase.table('auctions').select('name', 'description', 'status', 'start_date', 'start_time', 'starting_price', 'end_date', 'end_time', 'auction_type', 'image_url').eq('id', auction_id).execute()
#         item = response.data[0] if response.data else {} 

#         if not item:
#                 return jsonify({'error': 'Auction not found'}), 404

#         bid_response = (
#                     supabase.table('bids')
#                     .select('bid_amount')
#                     .eq('auction_id', auction_id)
#                     .order('bid_amount', desc=True)
#                     .limit(1)
#                     .execute()
#         )
#         max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None
#         item["max_bid"] = max_bid 
#         latest_max_bid = max_bid
#         if not polling_thread_started:
#             polling_thread_started = True
#             threading.Thread(target=poll_for_new_bids, daemon=True).start()

#         return jsonify(item), 200
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 500

@productPage.route('/place_bid', methods=['POST'])
def place_bid():
    print("Received bid request:", request.json)  # Debugging log
    data = request.json
    # The frontend sends auctionId and bidPrice
    bid_price = data.get('bidPrice')

    print("current_auction_id is:", current_auction_id) # debug

    if bid_price is None:
        return jsonify({'error': 'bidPrice are required'}), 400

    try:
        new_bid = {
            'user_id': "b7f65d95-7589-4dca-a389-5e293bd648e4", # hard-code for now
            'auction_id': current_auction_id,
            'bid_amount': bid_price,
            'created_at': datetime.datetime.utcnow().isoformat() 
        }
        response = supabase.table('bids').insert(new_bid).execute()

        # Emit WebSocket event when a new bid is placed
        requests.post(f"{API_GATEWAY_URL}/bid_update", json={
            "auction_id": current_auction_id,
            "max_bid": bid_price
        })

        return jsonify({'message': 'Bid placed successfully', 'bid': response.data}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
def poll_for_new_bids():
    global current_auction_id, latest_max_bid
    print("Polling thread started!")
    while True:
        print("Polling loop running...")
        if not current_auction_id:
            print("No auction selected. Waiting...")
            time.sleep(1)
            continue  # Skip iteration if no auction is set

        try:
            print(f"Checking for new bids on auction: {current_auction_id}")
            # Get the latest highest bid
            bid_response = (
                supabase.table('bids')
                .select('bid_amount')
                .eq('auction_id', current_auction_id)
                .order('bid_amount', desc=True)
                .limit(1)
                .execute()
            )
            print(f"Bid response from DB: {bid_response.data}")
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

                print(f"New bid detected for auction {current_auction_id}: {new_max_bid}")

        except Exception as e:
            print("Error polling bids:", e)

        time.sleep(2)  # Wait 5 seconds before checking again




# if __name__ == "__main__":
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True) 

# @app.route('/product', methods=['GET'])
# def product():
#     # data = request.json
#     # auction_id = data.get('auction_id')

#     global current_auction_id, latest_max_bid, polling_thread_started
#     auction_id = "b3dd3d7f-1f20-4f79-9651-b33b9f411600"
#     current_auction_id = auction_id

#     if not auction_id:
#         return jsonify({'error': 'auction_id is required'}), 400
#     try:
#         response = supabase.table('auctions').select('name', 'description', 'status', 'end_date', 'end_time', 'auction_type', 'image_url').eq('id', auction_id).execute()
#         item = response.data[0] if response.data else {} 

#         if not item:
#                 return jsonify({'error': 'Auction not found'}), 404

#         bid_response = (
#                     supabase.table('bids')
#                     .select('bid_amount')
#                     .eq('auction_id', auction_id)
#                     .order('bid_amount', desc=True)
#                     .limit(1)
#                     .execute()
#         )
#         max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None
#         item["max_bid"] = max_bid 
#         latest_max_bid = max_bid
#         if not polling_thread_started:
#             polling_thread_started = True
#             threading.Thread(target=poll_for_new_bids, daemon=True).start()

#         return jsonify({'item': item}), 200
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 500

# def poll_for_new_bids():
#     global current_auction_id, latest_max_bid
#     print("Polling thread started!")
#     while True:
#         print("Polling loop running...")
#         if not current_auction_id:
#             print("No auction selected. Waiting...")
#             time.sleep(1)
#             continue  # Skip iteration if no auction is set

#         try:
#             print(f"Checking for new bids on auction: {current_auction_id}")
#             # Get the latest highest bid
#             bid_response = (
#                 supabase.table('bids')
#                 .select('bid_amount')
#                 .eq('auction_id', current_auction_id)
#                 .order('bid_amount', desc=True)
#                 .limit(1)
#                 .execute()
#             )
#             print(f"Bid response from DB: {bid_response.data}")
#             new_max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None

#             # Only send update if bid amount has changed
#             if new_max_bid != latest_max_bid:
#                 latest_max_bid = new_max_bid
#                 socketio.emit('bid_update', {'auction_id': current_auction_id, 'max_bid': new_max_bid})
#                 print(f"New bid detected for auction {current_auction_id}: {new_max_bid}")

#         except Exception as e:
#             print("Error polling bids:", e)

#         time.sleep(2)  # Wait 5 seconds before checking again




# if __name__ == "__main__":
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True) 

# # @app.route('/product', methods=['GET'])
# # def product():
# #     # data = request.json
# #     # auction_id = data.get('auction_id')

# #     global current_auction_id, latest_max_bid
# #     auction_id = "b3dd3d7f-1f20-4f79-9651-b33b9f411600"
# #     current_auction_id = auction_id

# #     if not auction_id:
# #         return jsonify({'error': 'auction_id is required'}), 400
# #     try:
# #         response = supabase.table('auctions').select('name', 'description', 'status', 'end_date', 'end_time', 'auction_type', 'image_url').eq('id', auction_id).execute()
# #         item = response.data[0] if response.data else {} 

# #         if not item:
# #                 return jsonify({'error': 'Auction not found'}), 404

# #         bid_response = (
# #                     supabase.table('bids')
# #                     .select('bid_amount')
# #                     .eq('auction_id', auction_id)
# #                     .order('bid_amount', desc=True)
# #                     .limit(1)
# #                     .execute()
# #         )
# #         max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None
# #         item["max_bid"] = max_bid 

# #         return jsonify({'item': item}), 200

# #     except Exception as e:
# #         traceback.print_exc()
# #         return jsonify({'error': str(e)}), 500

# # def listen_for_bids():
# #     def handle_bids(payload):
# #         global current_auction_id
# #         # Extract auction_id and new max bid
# #         new_auction_id = payload["record"]["auction_id"]

# #         if new_auction_id != current_auction_id:
# #             return  # Ignore updates for other auctions

# #         print(f"New bid detected for auction {new_auction_id}") # debug

# #         # Fetch the new highest bid
# #         bid_response = (
# #             supabase.table('bids')
# #             .select('bid_amount')
# #             .eq('auction_id', new_auction_id)
# #             .order('bid_amount', descending=True)
# #             .limit(1)
# #             .execute()
# #         )
# #         new_max_bid = bid_response.data[0]['bid_amount'] if bid_response.data else None

# #         # Broadcast the new max bid to all connected clients
# #         socketio.emit('bid_update', {'auction_id': new_auction_id, 'max_bid': new_max_bid}, broadcast=True)

# #     # Subscribe to the "bids" table for inserts
# #     supabase.table("bids").on("INSERT", handle_bids).subscribe()


# # # Start the Realtime Listener in a Separate Thread
# # threading.Thread(target=listen_for_bids, daemon=True).start()


