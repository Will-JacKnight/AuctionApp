import pandas as pd
import random
import sys
from flask import Flask, request, Blueprint, jsonify
from supabase_client import supabase # need to modify
from datetime import datetime, timezone
# *************  DESCRIPTION: ********************************
# This page handles requests from the user to search items
# *************************************************************

# Create a Flask Blueprint named "mainPage" for the items displayed on the main page
mainPage = Blueprint("mainPage", __name__)

# Fetch highest bids in one query (avoiding per-item queries) and update expired items
def return_items_with_max_bid(items, update_expire = True):

    auction_ids = [item['id'] for item in items]
    
    # Raw SQL in Supabase SQL Function Editor
    """
        CREATE OR REPLACE FUNCTION get_max_bids(auction_ids UUID[]) 
        RETURNS TABLE(auction_id UUID, max_bid DECIMAL) AS $$
        BEGIN
            RETURN QUERY 
            SELECT b.auction_id, MAX(b.bid_amount) AS max_bid
            FROM bids b
            WHERE b.auction_id = ANY(auction_ids)
            GROUP BY b.auction_id;
        END;
        $$ LANGUAGE plpgsql;
    """

    # Execute the raw SQL query using Supabase's `rpc` method
    bid_response = supabase.rpc('get_max_bids', {
        "auction_ids": auction_ids
    }).execute()

    # Create a dictionary of auction_id -> max_bid for fast lookup
    bid_data = {bid['auction_id']: bid['max_bid'] for bid in bid_response.data}

    # Create a list of auction ids to mark as expired
    current_time = datetime.now(timezone.utc)

    expired_auction_ids = [
        item['id'] for item in items
        if datetime.fromisoformat(f"{item['end_date']}T{item['end_time']}Z".replace("Z", "+00:00")) <= current_time
    ]

    if update_expire and expired_auction_ids:
        update_expired_response = (
            supabase.table('auctions')
            .update({"status": "expired"})
            .in_('id', expired_auction_ids)
            .execute()
        )
        print(f"Updated {update_expired_response.count} auctions as expired.")

    # Process active auctions
    active_items = [
        {
            **item,
            "max_bid": bid_data.get(item["id"]),
            "remaining_days": max(0, int(
                (datetime.fromisoformat(f"{item['end_date']}T{item['end_time']}Z".replace("Z", "+00:00")) - current_time
            ).total_seconds() // 86400))
        }
        for item in items if item['id'] not in expired_auction_ids
    ]

    return active_items

# Define a route for searching items with keyword
@mainPage.route('/search', methods=['GET', 'POST'])
def search_item():
    # Get keyword from query parameter
    data = request.get_json()
    keyword = data.get("query", "")
    print(keyword)

    # Fetch items matching the search query
    response = (
        supabase.table('auctions')
        .select('name', 'starting_price', 'image_url', 'id', 'category', 'end_date', 'end_time', 'status')
        .ilike('name', f"%{keyword}%")
        .execute()
    )
    
    items = response.data
    # Fetch highest bids in one query (avoiding per-item queries)
    active_items = return_items_with_max_bid(items, update_expire = False) 
    
    return jsonify(active_items), 200


# Define a route for searching items with keyword
@mainPage.route('/search_byTag', methods=['GET', 'POST'])
def search_item_byTag():
    # Get keyword from query parameter
    data = request.get_json()
    keyword = data.get("query_tag", "")
    print(keyword)
    sys.stdout.flush()

    # Fetch items matching the search query
    response = (
        supabase.table('auctions')
        .select('name', 'starting_price', 'image_url', 'id', 'category', 'end_date', 'end_time', 'status')
        .ilike('category', f"%{keyword}%")
        .execute()
    )
    
    items = response.data
    # Fetch highest bids in one query (avoiding per-item queries)
    active_items = return_items_with_max_bid(items, update_expire = False) 
    
    return jsonify(active_items), 200


# Define a route for displaying default items on the mainpage
@mainPage.route('/display_mainPage', methods=['GET'])
def display_item():
    
    # Fetch all matching products from Supabase
    response = supabase.table('auctions').select('name', 'starting_price', 'image_url', 'id', 'end_date', 'end_time').execute()
    items = response.data

    if not items:
        return jsonify([])  # Return an empty list if no items
    
    # Fetch highest bids in one query (avoiding per-item queries)
    active_items = return_items_with_max_bid(items, update_expire = True) 

    return jsonify(active_items)  # Return only active items


    

