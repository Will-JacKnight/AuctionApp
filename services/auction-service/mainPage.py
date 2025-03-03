import pandas as pd
import random
from flask import Flask, request, Blueprint, jsonify
from supabase_client import supabase # need to modify
from datetime import datetime, timezone
# *************  DESCRIPTION: ********************************
# This page handles requests from the user to search items
# *************************************************************

# Create a Flask Blueprint named "mainPage" for the items displayed on the main page
mainPage = Blueprint("mainPage", __name__)

# Define a route for searching items with keyword
@mainPage.route('/search', methods=['GET', 'POST'])
def search_item():
    """Search for items by keyword, check expiration status, and fetch similar active items if needed."""
    
    # Get search keyword
    data = request.get_json()
    keyword = data.get("query", "").strip()
    print(f"Search Query: {keyword}")

    # Fetch items matching the search query
    response = (
        supabase.table('auctions')
        .select('name', 'starting_price', 'image_url', 'id', 'category', 'end_date', 'end_time', 'status')
        .ilike('name', f"%{keyword}%")
        .execute()
    )
    
    search_results = response.data
    active_items = []

    # Get the current UTC time
    current_time = datetime.now(timezone.utc)

    for item in search_results:
        # Combine end_date and end_time into a full timestamp
        end_datetime_str = f"{item['end_date']}T{item['end_time']}Z"
        end_datetime = datetime.fromisoformat(end_datetime_str.replace("Z", "+00:00"))

        # Calculate remaining days
        remaining_time_delta = (end_datetime - current_time).total_seconds()
        item['remaining_days'] = max(0, int(remaining_time_delta // 86400))

        # Check if auction is expired
        if end_datetime <= current_time:
            # Mark as expired in the database
            supabase.table('auctions').update({"status": 'expired'}).eq('id', item['id']).execute()
            print(f"Auction {item['id']} marked as expired.")
        else:
            # Fetch max bid for active items
            bid_response = (
                supabase.table('bids')
                .select('bid_amount')
                .eq('auction_id', item['id'])
                .order('bid_amount', desc=True)
                .limit(1)
                .execute()
            )
            item['max_bid'] = bid_response.data[0]['bid_amount'] if bid_response.data else None

            active_items.append(item)

    # # Fetch similar items if there are fewer than 12 active results
    # if len(active_items) < 12:
    #     # Extract categories from active search results
    #     categories = set(item["category"] for item in active_items if "category" in item)

    #     # Query similar items based on category
    #     similar_response = (
    #         supabase.table('auctions')
    #         .select('name', 'starting_price', 'image_url', 'id', 'category', 'end_date', 'end_time', 'status')
    #         .or_(
    #             " or ".join([f"category.ilike.%{cat}%" for cat in categories])
    #         )
    #         .execute()
    #     )

    #     similar_items = similar_response.data

    #     # Process similar items and exclude expired ones
    #     for item in similar_items:
    #         end_datetime_str = f"{item['end_date']}T{item['end_time']}Z"
    #         end_datetime = datetime.fromisoformat(end_datetime_str.replace("Z", "+00:00"))

    #         # Calculate remaining days
    #         remaining_time_delta = (end_datetime - current_time).total_seconds()
    #         item['remaining_days'] = max(0, int(remaining_time_delta // 86400))

    #         if end_datetime > current_time and item.get("status") != "expired":
    #             # Fetch max bid for similar items
    #             bid_response = (
    #                 supabase.table('bids')
    #                 .select('bid_amount')
    #                 .eq('auction_id', item['id'])
    #                 .order('bid_amount', desc=True)
    #                 .limit(1)
    #                 .execute()
    #             )
    #             item['max_bid'] = bid_response.data[0]['bid_amount'] if bid_response.data else None

    #             active_items.append(item)

    #         # Ensure max 12 active items in the final response
    #         if len(active_items) >= 12:
    #             break

    return jsonify(active_items), 200

# Define a route for displaying default items on the mainpage
@mainPage.route('/display_mainPage', methods=['GET'])
def display_item():
    
    # Fetch all matching products from Supabase
    response = supabase.table('auctions').select('name', 'starting_price', 'image_url', 'id', 'end_date', 'end_time').execute()
    items = response.data

    if not items:
        return jsonify([])  # Return an empty list if no items
    
    # Get the current UTC time
    current_time = datetime.now(timezone.utc)

    active_items = []

    for item in items:
        # Combine end_date and end_time into a full timestamp
        end_datetime_str = f"{item['end_date']}T{item['end_time']}Z"
        end_datetime = datetime.fromisoformat(end_datetime_str.replace("Z", "+00:00"))  # Convert to datetime object
         # Calculate remaining days
        remaining_time_delta = (end_datetime - current_time).total_seconds()
        remaining_days = max(0, int(remaining_time_delta // 86400))

        # Check if auction is still active
        if end_datetime <= current_time and item.get("status") != "expired":
            update_response = (
                supabase.table('auctions')
                .update({"status": 'expired'})  # Update status to "expired"
                .eq('id', item['id'])  # Where id matches the item's id
                .execute()
            )
            print(f"Auction {item['id']} marked as expired.")

        else:
            auction_id = item['id']

            # Get the highest bid for the current auction
            bid_response = (
                supabase.table('bids')
                .select('bid_amount')
                .eq('auction_id', auction_id)
                .order('bid_amount', desc=True)  # Sort in descending order
                .limit(1)  # Get only the highest bid
                .execute()
            )

            # Attach max_bid if available, otherwise keep it None
            item['max_bid'] = bid_response.data[0]['bid_amount'] if bid_response.data else None
            item['remaining_days'] = remaining_days
            # Add active item to the list
            active_items.append(item)

    return jsonify(active_items)  # Return only active items


    # # Duplicate items until we have at least 12
    # while len(items) < 12:
    #     items += items[:12 - len(items)]  # Add copies of existing items

    # # Shuffle and pick exactly 12 random items
    # random_items = random.sample(items, 12)

    # return jsonify()


    

