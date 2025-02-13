from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from supabase import create_client, Client
import os
import bcrypt
import datetime
from functools import wraps
from dotenv import load_dotenv
from flask_cors import CORS
# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure JWT settings
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")  # Retrieve the secret key from environment variables
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=24)  # Set token expiration time to 24 hours
jwt = JWTManager(app)

# Supabase Setting
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### **User Registration API **
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

# Check if username exists using Supabase
    existing_user = supabase.table("users").select("*").eq("username", username).execute()
    if existing_user.data:
        return jsonify({"error": "Username already exists"}), 400
    
    # Check if the email already exists
    existing_user = supabase.table("users").select("*").eq("email", email).execute()
    if existing_user.data:
        return jsonify({"error": "Email already registered"}), 409

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Save user data to Supabase
    new_user = supabase.table("users").insert({
        "email": email,
        "password": hashed_password,
        "username": username,
        "address": address,
        "phone": phone,
        "surname": surname,
        "firstname": firstname,
        "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }).execute()

    return jsonify({"message": "User registered successfully. Please log in."}), 201

### **User Login API**
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email').lower() 
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    try:
        # Retrieve only required fields (`id`, `password`, `username`)
        user_query = supabase.table("users").select("id, password, username").eq("email", email).execute()

        if not user_query.data:
            return jsonify({"error": "User not found"}), 404

        user = user_query.data[0]
        hashed_password = user["password"]

        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({"error": "Invalid password"}), 401

        # Generate Access Token & Refresh Token
        access_token = create_access_token(identity=user["id"])

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "username": user["username"]
        }), 200
    
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


### **Protected API Route (Requires JWT Token)**
@app.route('/protected', methods=['GET'])
@jwt_required()  # Automatically handles token verification
def protected():
    user_id = get_jwt_identity()  # Retrieve `user_id` from JWT Token
    return jsonify({"message": "You have access to this protected route!", "user_id": user_id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)