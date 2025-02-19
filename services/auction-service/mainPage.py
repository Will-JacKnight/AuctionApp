import pandas as pd
import random
from flask import Flask, request, Blueprint, jsonify
from supabase_client import supabase # need to modify

# *************  DESCRIPTION: ********************************
# This page handles requests from the user to search items
# *************************************************************

# Create a Flask Blueprint named "mainPage" for the items displayed on the main page
mainPage = Blueprint("mainPage", __name__)

# Define a route for searching items with keyword
@mainPage.route('/search', methods=['GET', 'POST'])
def search_item():
    # Get keyword from query parameter
    data = request.get_json()
    keyword = data.get("query", "")
    print(keyword)

    # Query auctions table with filtering
    response = supabase.table('auctions').select('item_name', 'starting_price', 'image_url').ilike('item_name', f"%{keyword}%").execute()

    # Return JSON response

    return jsonify(response.data), 200

# Define a route for displaying default items on the mainpage
@mainPage.route('/display_mainPage', methods=['GET'])
def display_item():
    
    # Fetch all matching products from Supabase
    response = supabase.table('auctions').select('item_name', 'starting_price', 'image_url').execute()

    items = response.data  # List of items

    if not items:
        return jsonify([])  # Return an empty list if no items

    # Duplicate items until we have at least 12
    while len(items) < 12:
        items += items[:12 - len(items)]  # Add copies of existing items

    # Shuffle and pick exactly 12 random items
    random_items = random.sample(items, 12)

    return jsonify(random_items)


    

