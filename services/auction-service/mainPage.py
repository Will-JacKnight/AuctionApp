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
@mainPage.route('/search', methods=['GET'])
def search_item():
    # Get keyword from query parameter
    keyword = request.args.get('keyword', '')

    # Query auctions table with filtering
    response = supabase.table('auctions').select('*').ilike('item_name', f"%{keyword}%").execute()

    # Return JSON response
    return jsonify(response.data), 200

# Define a route for displaying default items on the mainpage
@mainPage.route('/display_mainPage')
def display_item():
    
    # Fetch all matching products from Supabase
    response = supabase.table('auctions').select('*').execute()

    # Shuffle and pick 12 random items (or return all if less than 12)
    random_items = random.sample(response.data, min(len(response.data), 12))

    return jsonify(random_items)


# Run the app if this is the main module
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7070)
    

