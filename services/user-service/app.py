from flask import Flask, request, jsonify
from supabase import create_client, Client
import os
import bcrypt
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv

app = Flask(__name__)

# Supabase Setting
SUPABASE_URL = "https://fyzhnlztyjbwdujmzwys.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5emhubHp0eWpid2R1am16d3lzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkzNzAwMTIsImV4cCI6MjA1NDk0NjAxMn0.81BmyFNudLn95_aaDwny_0tIsaItxQEiW3aDuj-3xYE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT key 
SECRET_KEY = "6b4b9dc211b66ce60b58f731f1465e3c09537c3ce3499453ee0a12ddbb3073f3"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json  # Read the data sent from frontend
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    address = data.get('address', '')
    phone = data.get('phone', '')
    surname = data.get('surname', '')
    firstname = data.get('firstname', '')

    # Make sure non-null
    if not email or not password or not username:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the email already exists
    existing_user = supabase.table("users").select("*").eq("email", email).execute()
    if existing_user.data:
        return jsonify({"error": "Email already registered"}), 409

    # Hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Save into Supabase
    new_user = supabase.table("users").insert({
        "email": email,
        "password": hashed_password,
        "username": username,
        "address": address,
        "phone": phone,
        "surname": surname,
        "firstname": firstname,
        "created_at": datetime.datetime.utcnow()
    }).execute()

    # Generate WT Token
    token = jwt.encode(
        {
            "user_id": new_user.data[0]["id"], # User ID
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Setting the expire time
        }, 
        SECRET_KEY, # Using the secret key to encode
        algorithm="HS256")

    # Return the token to frontend
    return jsonify({"message": "User created successfully", "token": token}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email').lower() 
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    
    user = supabase.table("users").select("*").eq("email", email).execute()

    if not user.data:
        return jsonify({"error": "User not found"}), 404

    user = user.data[0]
    hashed_password = user["password"]

    # Verify the password
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return jsonify({"error": "Invalid password"}), 401

    # Generate JWT Token
    token = jwt.encode({"user_id": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token}), 200

# Token verification decorator
def token_required(f):
    @wraps(f) # Ensures the original function metadata is preserved
    def decorated(*args, **kwargs):
        # Retrieve the token from the request headers (Authorization: Bearer <token>)
        token = request.headers.get('Authorization')

        # If no token is provided, return 401 Unauthorized
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            token = token.split(" ")[1] if "Bearer " in token else token

            # Decode the JWT token using the SECRET_KEY and HS256 algorithm
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # Store `user_id` in the request object so it can be accessed in the protected route
            request.user_id = decoded["user_id"]
            
        except jwt.ExpiredSignatureError:
            # If the token has expired, return 401 Unauthorized
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            # If the token is invalid, return 401 Unauthorized
            return jsonify({"error": "Invalid Token"}), 401
        return f(*args, **kwargs)
    return decorated

# Test for protected API route that requires a valid JWT token to access
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({"message": "You have access to this protected route!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 